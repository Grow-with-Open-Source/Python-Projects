#!/usr/bin/env python3

import os
import re
from typing import Dict
from datetime import datetime, timedelta, timezone
from googleapiclient.discovery import build
from google import genai
from dotenv import load_dotenv
import isodate


# Load keys from .env file
load_dotenv()

# ——— ENV variables ———
YT_API_KEY = os.environ.get('YT_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# ——— CONSTANTS ———
SERVICE_TYPE = 'youtube'
SERVICE_VERSION = 'v3'
MODEL_NAME = 'gemini-1.5-flash'

DEFAULT_MAX_API_CALLS = 5
DEFAULT_MAX_RESULTS_PER_PAGE = 50
DEFAULT_MAX_RESULTS = 5
DEFAULT_MIN_VIDEO_DURATION_MINUTES = 10
DEFAULT_MAX_VIDEO_DURATION_MINUTES = 60
DEFAULT_NO_OF_PREV_DAYS = 14

REGEX_PATTERN = r'\b(10|[1-9](\.\d+)?|0?\.\d+)\b'
DEFAULT_SCORE = 5.0


class TimeUtils:
    """
    Utility class for handling time-related calculations for YouTube videos.
    """
    @staticmethod
    def get_timestamp_n_days_from_now(days: int) -> str:
        """
        Get the timestamp for a date N days ago in ISO 8601 format.
        """
        date_before_n_days = datetime.now(timezone.utc) - timedelta(days=days)
        formatted_date = date_before_n_days.isoformat('T').replace('+00:00', 'Z')
        return formatted_date

    @staticmethod
    def is_duration_in_mins(duration: str) -> bool:
        """
        Return True if the duration string contains hours or does not contain minutes.
        Used to filter out videos that are too short or too long.
        """
        return 'H' in duration or 'M' not in duration

    @staticmethod
    def derive_total_seconds_from_duration(duration: str) -> int:
        """
        Convert ISO 8601 duration (e.g., 'PT5M30S') to total seconds.
        """
        import isodate
        try:
            total_seconds = int(isodate.parse_duration(duration).total_seconds())
        except Exception as e:
            print(f"Failed to parse duration {duration}: {e}")
            total_seconds = 0
        return total_seconds

    @staticmethod
    def is_video_duration_in_range(
            total_seconds: int,
            *,
            min_duration: int = DEFAULT_MIN_VIDEO_DURATION_MINUTES,
            max_duration: int = DEFAULT_MAX_VIDEO_DURATION_MINUTES) -> bool:
        """
        Return True if the video duration is within min and max minutes.
        """
        return min_duration * 60 <= total_seconds <= max_duration * 60


class VideoDetailsExtractor:
    """
    A class to encapsulate YouTube video extraction logic.
    This class can be extended or modified for more complex behaviors.
    """

    __platform_conn = build(
        serviceName=SERVICE_TYPE,
        version=SERVICE_VERSION,
        developerKey=YT_API_KEY
    )

    def __init__(
            self,
            query: str,
            *,
            no_prev_days: int = DEFAULT_NO_OF_PREV_DAYS,
            max_pages: int = DEFAULT_MAX_API_CALLS,
            max_results: int = DEFAULT_MAX_RESULTS) -> None:
        """
        Initialize the VideoDetailsExtractor.
        """
        self.__filtered_videos = []
        self.__next_page_token = None
        self.__page_count = 0
        self.__max_pages = max_pages

        self.query = query
        self.__targeted_date = TimeUtils.get_timestamp_n_days_from_now(no_prev_days)
        self.__max_results = max_results

        self.__search_response = self.get_new_search_response()
        self.scan_videos()

    def get_new_search_response(self) -> dict:
        """
        Fetch a new search response for the given query.
        """
        search_config = {
            "q": self.query,
            "part": "id,snippet",
            "type": "video",
            "order": "relevance",
            "publishedAfter": self.__targeted_date,
            "maxResults": DEFAULT_MAX_RESULTS_PER_PAGE,
            "pageToken": self.__next_page_token
        }

        new_search_response = VideoDetailsExtractor.__platform_conn \
            .search() \
            .list(**search_config) \
            .execute()

        self.__page_count += 1

        return new_search_response

    def get_video_ids_from_search_response(self) -> list:
        """
        Extract video IDs from the current search response.
        """
        items_list = self.__search_response.get('items', [])
        return [item['id']['videoId'] for item in items_list]

    def filter_videos(self) -> None:
        """
        Filter videos based on duration and recency.
        Adds filtered video details to self.__filtered_videos.
        """
        video_ids = self.get_video_ids_from_search_response()
        if not video_ids:
            print("No video IDs found in the search response.")
            return

        # Fetch full video details
        details_config = {
            "part": "contentDetails,snippet",
            "id": ",".join(video_ids)
        }

        details = VideoDetailsExtractor.__platform_conn.videos().list(**details_config).execute()

        for item in details.get('items', []):
            try:
                duration = item['contentDetails']['duration']
                
                # Skip videos with hours or missing minutes
                if TimeUtils.is_duration_in_mins(duration):
                    continue

                # Convert duration to total seconds
                total_seconds = TimeUtils.derive_total_seconds_from_duration(duration)

                # Check if video is in the desired range
                if TimeUtils.is_video_duration_in_range(total_seconds):
                    video_details = {
                        'id': item['id'],
                        'title': item['snippet']['title'],
                        'duration': total_seconds,
                        'publishedAt': item['snippet']['publishedAt']
                    }
                    self.__filtered_videos.append(video_details)

                    # Stop if we reach the max results
                    if len(self.__filtered_videos) >= self.__max_results:
                        break

            except Exception as e:
                print(f"Error processing video {item.get('id', 'N/A')}: {e}")
                continue

        print(f"Filtered {len(self.__filtered_videos)} videos based on criteria.")

    def has_filtered_videos_reached_limit(self) -> bool:
        """
        Check if the maximum number of filtered videos has been reached.
        """
        return len(self.__filtered_videos) < self.__max_results

    def has_page_token_reached_limit(self) -> bool:
        """
        Check if the maximum number of API calls has been reached.
        """
        return self.__page_count < self.__max_pages

    def update_next_page_token(self) -> None:
        """
        Update the next page token based on the search response.
        """
        self.__next_page_token = self.__search_response.get('nextPageToken', None)

    def scan_videos(self) -> None:
        """
        Scan for videos that meet the specified criteria.
        This method keeps searching until it finds enough videos that meet the criteria
        or exhausts the search results.
        """
        # NOTE:
        # First search page is fetched but not filtered due to original pagination logic.
        # This is intentional to keep parity with the upstream source code.

        while self.has_filtered_videos_reached_limit() and self.has_page_token_reached_limit():
            self.__search_response = self.get_new_search_response()
            self.filter_videos()
            self.update_next_page_token()
            if not self.__next_page_token:
                break
    
    def get_video_details(self) -> list:
        """
        Fetch video details for a list of filtered video based that were previously computed.
        """
        if not self.__filtered_videos:
            print('No suitable videos found after applying filters.')
        return self.__filtered_videos


class GenModel:
    """
    A class to encapsulate the Gemini model for scoring video titles.
    This class can be extended or modified for more complex behaviors.
    """
    _model = None

    @classmethod
    def _initialize_model(cls):
        """
        Initialize the Gemini model if it hasn't been initialized yet.
        """
        if cls._model is None:
            #cls._client = genai.Client(api_key=GEMINI_API_KEY)
            #cls._model = cls._client

            cls._client = genai.Client(api_key=GEMINI_API_KEY)
            models = cls._client.models.list()
            print(models)


    @staticmethod
    def get_prompt_for_title(title: str, query: str) -> str:
        """
        Generate a prompt for the Gemini model to score the title based on the query.
        """
        return (
            f"Query: {query}\n"
            f"Title: {title}\n"
            "Rate relevance & quality 1–10 (just give the number)."
        )
    
    @classmethod
    def get_score_for_title(cls, title: str, query: str) -> float:
        """
        Get the score for a video title based on the query using the Gemini model.
        If the model is not initialized, it will initialize it first.
        If the score cannot be parsed, it returns a default score.
        """
        cls._initialize_model()
        prompt = cls.get_prompt_for_title(title, query)
        try:
            response = cls._model.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            score_text = response.text.strip()
            match = re.search(REGEX_PATTERN, score_text)
            return float(match.group()) if match else DEFAULT_SCORE
        
        except (ValueError, AttributeError):
            print(
                "[Warning] Gemini response could not be parsed. "
                "Using default relevance score."
            )
            return DEFAULT_SCORE
   
            
        except Exception as e:
            print(
                "[Warning] Gemini API call failed. "
                "Falling back to default relevance score."
            )
            return DEFAULT_SCORE


class VideoProcessor:
    """
    A class to process video details and rank them based on a scoring model.
    This class can be extended or modified for more complex behaviors.
    """
    def __init__(self, scorer=GenModel):
        """
        Initialize the VideoProcessor with a scoring model.
        """
        self.scorer = scorer

    def find_and_rank_videos(self, query: str, num_results: int = DEFAULT_MAX_RESULTS):
        """
        Find and rank videos based on the query.
        This method uses the VideoDetailsExtractor to find videos and the scoring model to rank them.
        """
        videos = VideoDetailsExtractor(query).get_video_details()
        if not videos:
            return []

        for video in videos:
            video['score'] = self.scorer.get_score_for_title(
                video['title'], query)

        return sorted(videos, key=lambda v: v['score'], reverse=True)[:num_results]


if __name__ == '__main__':
    required_env_vars = ['YT_API_KEY', 'GEMINI_API_KEY']
    missing = [v for v in required_env_vars if not os.environ.get(v)]

    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    user_query = input("Enter your search: ")

    video_processor = VideoProcessor()
    pick_best = video_processor.find_and_rank_videos(user_query)

    if not pick_best:
        print("No relevant videos found.")
    else:
        for idx, video in enumerate(pick_best, start=1):
            print(f"\n#{idx}")
            print(f"Title: {video['title']}")
            print(f"Score: {video['score']}")
            print(f"Published: {video['publishedAt']}")
