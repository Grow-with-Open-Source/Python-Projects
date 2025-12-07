# Stock Price Tracker 📈

A comprehensive Python application that tracks stock prices using Yahoo Finance API, visualizes daily/weekly trends with interactive charts, and sends automated Telegram notifications for price movements and alerts.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## ✨ Features

- 📊 **Real-time Stock Data**: Fetch live stock prices and historical data using Yahoo Finance API
- 📈 **Daily & Weekly Trends**: Visualize price movements over different timeframes
- 🎨 **Multiple Chart Types**: Line charts, candlestick charts, volume analysis, and summary reports
- 📱 **Telegram Alerts**: Receive instant notifications for price changes and threshold alerts
- 🎯 **Price Thresholds**: Set custom price alerts and get notified when triggered
- 📉 **Technical Analysis**: Moving averages, daily returns, and price distribution analysis
- 💾 **Export Functionality**: Save charts as PNG/HTML files for reporting
- 🖥️ **Command-line Interface**: Easy-to-use CLI with multiple options

## 📋 Requirements

- Python 3.8 or higher
- Internet connection (for fetching stock data)
- Telegram Bot (optional, for alerts)

## 🚀 Installation

1. **Clone or download this project**
   ```bash
   cd Stock-Price-Tracker
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Telegram Bot (Optional but recommended)**
   
   To receive price alerts via Telegram:
   
   - **Create a Telegram Bot:**
     1. Open Telegram and search for `@BotFather`
     2. Send `/newbot` command
     3. Follow instructions to create your bot
     4. Copy the **Bot Token** provided
   
   - **Get your Chat ID:**
     1. Start a chat with your new bot
     2. Search for `@userinfobot` on Telegram
     3. Start a chat and it will show your **Chat ID**
   
   - **Configure environment variables:**
     ```bash
     # Copy the example file
     cp config/.env.example config/.env
     
     # Edit config/.env and add your credentials
     TELEGRAM_BOT_TOKEN=your_bot_token_here
     TELEGRAM_CHAT_ID=your_chat_id_here
     ```

## 📖 Usage

### Basic Commands

**Track daily prices:**
```bash
python stock_tracker.py AAPL --daily
```

**Track weekly prices:**
```bash
python stock_tracker.py GOOGL --weekly
```

**Get stock information:**
```bash
python stock_tracker.py TSLA --info
```

### Advanced Usage

**Track with custom timeframe:**
```bash
# 60 days of daily data
python stock_tracker.py MSFT --daily --days 60

# 24 weeks of weekly data
python stock_tracker.py AMZN --weekly --weeks 24
```

**Save charts without displaying:**
```bash
python stock_tracker.py AAPL --daily --save-plots --no-plot
```

**Enable Telegram alerts:**
```bash
# Track with alert notification
python stock_tracker.py TSLA --daily --telegram --alert

# Check price threshold and alert
python stock_tracker.py AAPL --threshold 150 --threshold-type above --telegram
```

**Price threshold monitoring:**
```bash
# Alert when price goes above $200
python stock_tracker.py GOOGL --threshold 200 --threshold-type above --telegram

# Alert when price goes below $100
python stock_tracker.py MSFT --threshold 100 --threshold-type below --telegram
```

### Command-line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `ticker` | Stock ticker symbol (required) | - |
| `--daily` | Track daily prices | False |
| `--weekly` | Track weekly prices | False |
| `--days` | Number of days to track | 30 |
| `--weeks` | Number of weeks to track | 12 |
| `--plot` | Display plots | True |
| `--no-plot` | Don't display plots | False |
| `--save-plots` | Save plots to files | False |
| `--telegram` | Enable Telegram alerts | False |
| `--alert` | Send Telegram alert | False |
| `--threshold` | Price threshold for alerts | None |
| `--threshold-type` | Threshold type (above/below) | above |
| `--info` | Display stock info only | False |

## 📊 Example Output

### Console Output
```
============================================================
📈 STOCK PRICE TRACKER
============================================================
🔍 Validating ticker symbol: AAPL
✅ Ticker AAPL is valid

============================================================
📊 STOCK INFORMATION: AAPL
============================================================
Company:        Apple Inc.
Sector:         Technology
Industry:       Consumer Electronics
Current Price:  $178.45
Previous Close: $175.20
52W High:       $198.23
52W Low:        $124.17
Market Cap:     $2850.00B
============================================================

📈 Fetching 30 days of data for AAPL...
✅ Retrieved 30 days of data

────────────────────────────────────────────────────────────
📊 DAILY STATISTICS
────────────────────────────────────────────────────────────
Start Price:  $165.30
End Price:    $178.45
Change:       $13.15 (7.95%)
Highest:      $180.50
Lowest:       $164.90
────────────────────────────────────────────────────────────
```

### Telegram Alert Examples

**Daily Summary Alert:**
```
📊 DAILY SUMMARY: AAPL

📈 Overall: UP 7.95%

💰 Opening: $165.30
💵 Closing: $178.45
🔼 High: $180.50
🔽 Low: $164.90
📊 Change: $13.15 (+7.95%)

📅 Date: 2025-12-08 10:30:45
```

**Threshold Alert:**
```
🔔 THRESHOLD ALERT: AAPL

↗️ Price is now above $175.00!

💰 Current Price: $178.45
🎯 Threshold: $175.00

📅 Time: 2025-12-08 10:30:45
```

## 📁 Project Structure

```
Stock-Price-Tracker/
├── stock_tracker.py          # Main application
├── utils/
│   ├── __init__.py
│   ├── yahoo_finance.py      # Yahoo Finance API integration
│   ├── plotter.py            # Chart generation & visualization
│   └── telegram_alert.py     # Telegram bot integration
├── config/
│   └── .env.example          # Environment variables template
├── assets/
│   └── img/                  # Generated charts and screenshots
├── requirements.txt          # Python dependencies
└── README.md                 # Documentation
```

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **yfinance** | Yahoo Finance API for stock data |
| **pandas** | Data manipulation and analysis |
| **matplotlib** | Static chart generation |
| **plotly** | Interactive candlestick charts |
| **python-telegram-bot** | Telegram bot integration |
| **python-dotenv** | Environment variable management |

## 📈 Visualization Features

1. **Price Trend Chart**
   - Line chart with closing prices
   - 7-day and 30-day moving averages
   - Clean, professional styling

2. **Candlestick Chart**
   - Interactive OHLC (Open, High, Low, Close) visualization
   - Volume bar chart
   - Zoom and pan capabilities

3. **Volume Analysis**
   - Price vs. volume correlation
   - Average volume indicators
   - Color-coded volume bars

4. **Summary Report**
   - Comprehensive multi-panel view
   - Price statistics summary
   - Daily range visualization

## 🔔 Telegram Alerts

The app sends various types of alerts:

- **📊 Price Updates**: Regular stock price summaries
- **🚨 Threshold Alerts**: Notifications when price crosses set levels
- **📈 Daily Summaries**: End-of-day price reports with statistics
- **❌ Error Alerts**: Notifications for any issues or errors

## 🎯 Use Cases

- **Day Traders**: Monitor intraday price movements with alerts
- **Long-term Investors**: Track weekly trends and major price changes
- **Portfolio Monitoring**: Set threshold alerts for multiple stocks
- **Market Research**: Analyze historical trends and patterns
- **Automated Reporting**: Generate and save charts for presentations

## 🔍 Supported Stock Symbols

Any valid ticker symbol from Yahoo Finance, including:
- **US Stocks**: AAPL, GOOGL, MSFT, TSLA, AMZN, etc.
- **International**: Use country suffix (e.g., RELIANCE.NS for India)
- **ETFs**: SPY, QQQ, VTI, etc.
- **Cryptocurrencies**: BTC-USD, ETH-USD, etc.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Improve documentation
- Submit pull requests

## 📝 License

This project is open source and available for educational purposes.

## ⚠️ Disclaimer

This tool is for informational and educational purposes only. It should not be considered as financial advice. Always do your own research before making investment decisions.

## 👨‍💻 Author

Created as part of the [Python-Projects](https://github.com/Grow-with-Open-Source/Python-Projects) repository.

---

**Happy Trading! 📈💰**
