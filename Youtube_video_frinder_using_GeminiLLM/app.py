import os
import datetime
from googleapiclient.discovery import build
import google.generativeai as genai

# ——— CONFIG ———
# Initialize clients with environment variables
yt = build("youtube", "v3", developerKey=os.environ["YT_API_KEY"])

# Configure the Google Generative AI client
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash-latest')


def search_videos(query, max_filtered_results=20):
    """
    Search for YouTube videos matching a query, filtering by recency and duration.

    This function keeps searching until it finds enough videos that meet the criteria
    or exhausts the search results.
    """
    # Calculate publishedAfter timestamp (14 days ago)
    fourteen_days_ago = (datetime.datetime.utcnow()
                        - datetime.timedelta(days=14)).isoformat("T") + "Z"

    filtered_videos = []
    next_page_token = None
    page_count = 0
    max_pages = 5  # Limit the number of pages to search to avoid excessive API calls

    # Continue searching until we have enough filtered videos or run out of results
    while len(filtered_videos) < max_filtered_results and page_count < max_pages:
        # Step 1: Search for videos matching the query
        search_response = yt.search().list(
            q=query,
            part="id,snippet",
            type="video",
            order="relevance",
            publishedAfter=fourteen_days_ago,
            maxResults=50,  # Maximum allowed by the API
            pageToken=next_page_token
        ).execute()

        page_count += 1

        # Step 2: Collect video IDs from this page
        video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]

        # Break if no more videos found
        if not video_ids:
            break

        # Step 3: Get details for the fetched videos
        details = yt.videos().list(
            part="contentDetails,snippet",
            id=",".join(video_ids)
        ).execute()

        # Step 4: Filter by duration (4–20 minutes)
        for item in details.get("items", []):
            try:
                # Parse duration (ISO 8601 format, e.g. "PT5M30S")
                dur = item["contentDetails"]["duration"].replace("PT","")

                # Skip videos with hours or without minutes
                if "H" in dur or "M" not in dur:
                    continue

                # Split minutes and seconds
                parts = dur.split("M")
                mins = int(parts[0])
                secs = parts[1].replace("S","") if len(parts) > 1 else "0"
                seconds = int(secs) if secs else 0

                total_seconds = mins * 60 + seconds

                # Filter by duration (4 to 20 minutes inclusive)
                if 4 * 60 <= total_seconds <= 20 * 60:
                    filtered_videos.append({
                        "id": item["id"],
                        "title": item["snippet"]["title"],
                        "duration": total_seconds,
                        "publishedAt": item["snippet"]["publishedAt"]
                    })

                    # If we've found enough videos, we can stop
                    if len(filtered_videos) >= max_filtered_results:
                        break
            except Exception as e:
                print(f"Could not parse duration for video {item.get('id', 'N/A')}: {e}")
                continue

        # Check if there are more pages of results
        next_page_token = search_response.get("nextPageToken")
        if not next_page_token:
            break

        print(f"Found {len(filtered_videos)} qualifying videos so far. Searching next page...")

    print(f"Search completed. Found {len(filtered_videos)} videos meeting criteria.")
    return filtered_videos


def score_title(title, query):
    """Score a video title's relevance to the query using Gemini AI."""
    prompt = (
        f"Query: {query}\n"
        f"Title: {title}\n"
        "Rate relevance & quality 1–10 (just give the number)."
    )
    try:
        response = model.generate_content(prompt)
        score_text = response.text.strip()
        # Try to extract just the number if there's additional text
        import re
        match = re.search(r'\b([0-9]|10)(\.[0-9]+)?\b', score_text)
        if match:
            score = float(match.group(0))
        else:
            score = float(score_text)
        return score
    except ValueError:
        print(f"Model returned non-numeric score for '{title}': '{score_text}'")
        return 5.0  # Default middle score instead of 0
    except Exception as e:
        print(f"Error scoring title '{title}': {e}")
        if 'response' in locals() and hasattr(response, 'text'):
             print(f"API response text: {response.text}")
        return 5.0  # Default middle score


def pick_best(query, num_results=20):
    """
    Find and score the best YouTube videos for a query.

    Args:
        query: Search query string
        num_results: Number of top videos to return
    """
    # Get more videos than we need to ensure we have enough after scoring
    vids = search_videos(query, max_filtered_results=max(30, num_results * 1.5))

    if not vids:
        print("No suitable videos found after applying filters.")
        return

    # Score each video
    print(f"Scoring {len(vids)} videos...")
    for i, v in enumerate(vids):
        v["score"] = score_title(v["title"], query)
        print(f"  Scored video {i+1}/{len(vids)}: '{v['title']}' - Score: {v['score']:.2f}")

    # Sort by score in descending order
    vids.sort(key=lambda x: x.get("score", 0.0), reverse=True)

    # Print the top num_results
    result_count = min(num_results, len(vids))
    print(f"\n--- Top {result_count} Relevant Videos ---")

    for i, video in enumerate(vids[:num_results]):
        print(f"\n{i+1}.")
        print(f" • Title: {video.get('title', 'N/A')}")
        print(f" • URL:   https://youtu.be/{video.get('id', 'N/A')}")
        print(f" • Score: {video.get('score', 0.0):.2f}")
        duration_sec = video.get('duration', 0)
        print(f" • Duration: {duration_sec // 60}m{duration_sec % 60:02d}s")
        print(f" • Published: {video.get('publishedAt', 'N/A')}")


# —— RUN IT! ——
if __name__ == "__main__":
    # Check if API keys are set
    if "YT_API_KEY" not in os.environ or "GEMINI_API_KEY" not in os.environ:
        print("Error: YouTube and/or Gemini API keys not set in environment variables.")
    else:
        user_query = input("Enter your search (voice-to-text or text): ")
        # Call pick_best with the desired number of results
        pick_best(user_query, num_results=20)
