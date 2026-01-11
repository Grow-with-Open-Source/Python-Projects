# YouTube Relevance Finder with Gemini AI (Enhanced Version)

This Python application searches YouTube for recent videos based on a user query
and ranks them by relevance using Google’s Gemini AI model and the YouTube Data API.

---

## 🔍 Features

- Searches YouTube for videos published within the last 14 days
- Filters videos by duration (10–60 minutes)
- Uses Gemini AI to score video title relevance to a search query
- Gracefully falls back to a default score if Gemini API calls fail
- Prints ranked video titles with relevance scores and publication dates

---

## 🆕 Differences from the Original Implementation

This version introduces several improvements compared to the original source code:

- **Graceful Gemini API fallback**  
  When the Gemini API is unavailable, rate-limited, or returns an unexpected
  response, the application assigns a default relevance score instead of failing.

- **Cleaner error handling**  
  SDK and API-related errors are handled internally and surfaced as clear,
  user-friendly warning messages.

- **Improved project structure**  
  The application logic is organized into dedicated classes for:
  - Time utilities
  - YouTube video extraction and filtering
  - Gemini-based scoring
  - Video ranking and processing

- **Explicit documentation of limitations**  
  Known API constraints and fallback behavior are documented to reflect
  real-world usage conditions.

These changes make the project more robust and suitable for learning and experimentation.

---

## 🛠️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

2. Install dependencies
pip install google-api-python-client google-generativeai

3. Set up environment variables
Create a .env file or export in your terminal:
export YT_API_KEY=your_youtube_api_key
export GEMINI_API_KEY=your_gemini_api_key

🚀 Usage
Run the script:
python app.py

You will be prompted to enter a search query.
The script will then display a list of the top relevant YouTube videos.

📄 Example Output
Enter your search: Brazilian Jiu Jitsu
Filtered 5 videos based on criteria.
[Warning] Gemini API call failed. Falling back to default relevance score.

#1
Title: The New Face of Brazilian Jiu-Jitsu
Score: 5.0
Published: 2026-01-08T16:16:56Z

📌 Notes & Known Limitations
Valid API keys are required for:
YouTube Data API v3
Google Gemini API
Gemini API usage is subject to quota limits and model availability
When Gemini scoring fails, a default relevance score is applied so the
application can continue running without interruption
This fallback behavior is intentional and documented for learning purposes

🎯 Purpose of This Project
This project was contributed as part of an open-source learning journey to demonstrate:
API integration with third-party services
Defensive programming and graceful error handling
Clean project organization and documentation
Real-world constraints when working with LLM APIs
