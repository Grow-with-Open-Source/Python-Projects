"""
Telegram Alert System
Send stock price alerts via Telegram bot
"""

import os
from typing import Optional, Dict, Any
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
import asyncio


class TelegramAlert:
    """Send alerts via Telegram bot"""
    
    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        """
        Initialize Telegram bot
        
        Args:
            bot_token (str): Telegram bot token from @BotFather
            chat_id (str): Telegram chat ID to send messages to
        """
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = chat_id or os.getenv('TELEGRAM_CHAT_ID')
        
        if not self.bot_token or not self.chat_id:
            print("⚠️  Warning: Telegram credentials not configured")
            print("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env file")
            self.bot = None
        else:
            self.bot = Bot(token=self.bot_token)
    
    def is_configured(self) -> bool:
        """Check if Telegram bot is properly configured"""
        return self.bot is not None
    
    async def send_message_async(self, message: str) -> bool:
        """
        Send a text message via Telegram (async)
        
        Args:
            message (str): Message to send
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_configured():
            print("Telegram bot not configured. Skipping alert.")
            return False
        
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='HTML'
            )
            return True
        except TelegramError as e:
            print(f"Error sending Telegram message: {e}")
            return False
    
    def send_message(self, message: str) -> bool:
        """
        Send a text message via Telegram (sync wrapper)
        
        Args:
            message (str): Message to send
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_configured():
            print("Telegram bot not configured. Skipping alert.")
            return False
        
        try:
            # Run async function in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.send_message_async(message))
            loop.close()
            return result
        except Exception as e:
            print(f"Error in sync message send: {e}")
            return False
    
    def format_stock_alert(self, ticker: str, stats: Dict[str, Any], 
                          alert_type: str = "update") -> str:
        """
        Format stock data into a nice alert message
        
        Args:
            ticker (str): Stock ticker symbol
            stats (dict): Stock statistics
            alert_type (str): Type of alert ('update', 'threshold', 'daily_summary')
        
        Returns:
            str: Formatted message
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Emoji based on price change
        change_percent = stats.get('change_percent', 0)
        if change_percent > 0:
            emoji = "📈"
            direction = "UP"
        elif change_percent < 0:
            emoji = "📉"
            direction = "DOWN"
        else:
            emoji = "➡️"
            direction = "FLAT"
        
        if alert_type == "threshold":
            message = f"""
🚨 <b>PRICE ALERT: {ticker}</b> 🚨

{emoji} Price moved {direction} by {abs(change_percent):.2f}%!

💰 <b>Current Price:</b> ${stats.get('end_price', 'N/A')}
📊 <b>Previous Price:</b> ${stats.get('start_price', 'N/A')}
📉 <b>Change:</b> ${stats.get('change', 'N/A')} ({change_percent:+.2f}%)

📅 <b>Time:</b> {timestamp}
"""
        elif alert_type == "daily_summary":
            message = f"""
📊 <b>DAILY SUMMARY: {ticker}</b>

{emoji} Overall: {direction} {abs(change_percent):.2f}%

💰 <b>Opening:</b> ${stats.get('start_price', 'N/A')}
💵 <b>Closing:</b> ${stats.get('end_price', 'N/A')}
🔼 <b>High:</b> ${stats.get('highest', 'N/A')}
🔽 <b>Low:</b> ${stats.get('lowest', 'N/A')}
📊 <b>Change:</b> ${stats.get('change', 'N/A')} ({change_percent:+.2f}%)

📅 <b>Date:</b> {timestamp}
"""
        else:  # update
            message = f"""
📈 <b>Stock Update: {ticker}</b>

💰 <b>Current Price:</b> ${stats.get('end_price', 'N/A')}
📊 <b>Change:</b> ${stats.get('change', 'N/A')} ({change_percent:+.2f}%) {emoji}
🔼 <b>High:</b> ${stats.get('highest', 'N/A')}
🔽 <b>Low:</b> ${stats.get('lowest', 'N/A')}

📅 <b>Updated:</b> {timestamp}
"""
        
        return message.strip()
    
    def send_stock_alert(self, ticker: str, stats: Dict[str, Any], 
                        alert_type: str = "update") -> bool:
        """
        Send a formatted stock alert
        
        Args:
            ticker (str): Stock ticker symbol
            stats (dict): Stock statistics
            alert_type (str): Type of alert
        
        Returns:
            bool: True if successful
        """
        message = self.format_stock_alert(ticker, stats, alert_type)
        return self.send_message(message)
    
    def send_price_threshold_alert(self, ticker: str, current_price: float,
                                   threshold: float, threshold_type: str = "above") -> bool:
        """
        Send alert when price crosses a threshold
        
        Args:
            ticker (str): Stock ticker symbol
            current_price (float): Current stock price
            threshold (float): Price threshold
            threshold_type (str): 'above' or 'below'
        
        Returns:
            bool: True if successful
        """
        emoji = "🔔" if threshold_type == "above" else "⚠️"
        arrow = "↗️" if threshold_type == "above" else "↘️"
        
        message = f"""
{emoji} <b>THRESHOLD ALERT: {ticker}</b>

{arrow} Price is now <b>{threshold_type}</b> ${threshold:.2f}!

💰 <b>Current Price:</b> ${current_price:.2f}
🎯 <b>Threshold:</b> ${threshold:.2f}

📅 <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return self.send_message(message.strip())
    
    def send_error_alert(self, ticker: str, error_message: str) -> bool:
        """
        Send error notification
        
        Args:
            ticker (str): Stock ticker symbol
            error_message (str): Error description
        
        Returns:
            bool: True if successful
        """
        message = f"""
❌ <b>ERROR: {ticker}</b>

⚠️ <b>Issue:</b> {error_message}

📅 <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please check your stock tracker configuration.
"""
        
        return self.send_message(message.strip())
    
    def send_welcome_message(self, ticker: str) -> bool:
        """
        Send welcome/initialization message
        
        Args:
            ticker (str): Stock ticker symbol
        
        Returns:
            bool: True if successful
        """
        message = f"""
🚀 <b>Stock Price Tracker Started</b>

📊 Now tracking: <b>{ticker}</b>

You will receive alerts when:
• Significant price changes occur
• Daily summaries are available
• Threshold levels are crossed

💡 <i>Stay informed about your investments!</i>
"""
        
        return self.send_message(message.strip())
    
    async def test_connection_async(self) -> bool:
        """
        Test Telegram bot connection (async)
        
        Returns:
            bool: True if connection is successful
        """
        if not self.is_configured():
            return False
        
        try:
            bot_info = await self.bot.get_me()
            print(f"✅ Connected to Telegram bot: @{bot_info.username}")
            return True
        except TelegramError as e:
            print(f"❌ Failed to connect to Telegram: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        Test Telegram bot connection (sync wrapper)
        
        Returns:
            bool: True if connection is successful
        """
        if not self.is_configured():
            return False
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.test_connection_async())
            loop.close()
            return result
        except Exception as e:
            print(f"Error testing connection: {e}")
            return False
