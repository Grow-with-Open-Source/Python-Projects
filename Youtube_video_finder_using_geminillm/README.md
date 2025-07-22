"This is a Open source project initiated by me -you can fork, edit, and make a pull request" 

````markdown
# YouTube Relevance Finder with Gemini AI

This Python script searches YouTube for recent videos based on a user query and ranks them by relevance using Google's Gemini AI model. It filters results by duration and recency, scores video titles for relevance, and returns the top-ranked videos.

## 🔍 Features

- Searches YouTube for videos from the past 14 days
- Filters videos by duration (4–20 minutes)
- Uses Gemini AI to score title relevance to a query
- Prints the top relevant video links with scores and metadata

## 🛠️ Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
````

2. **Install dependencies**:

   ```bash
   pip install google-api-python-client google-generativeai
   ```

3. **Set up environment variables**:
   Create a `.env` file or export in terminal:

   ```bash
   export YT_API_KEY=your_youtube_api_key
   export GEMINI_API_KEY=your_gemini_api_key
   ```

## 🚀 Usage

Run the script:

```bash
python your_script_name.py
```

You'll be prompted to enter a search query. The script will then display a list of the top relevant YouTube videos based on that query.

## 📄 Example Output

```
1. 
 • Title: Learn Python in 10 Minutes
 • URL: https://youtu.be/xyz123
 • Score: 9.2
 • Duration: 10m30s
 • Published: 2025-05-01T12:34:56Z
```

## 📌 Notes

* Make sure you have valid API keys for both YouTube Data API v3 and Google Gemini.
* The script currently uses the `gemini-1.5-flash-latest` model.

## 📃 License

Open source – feel free to use and modify
