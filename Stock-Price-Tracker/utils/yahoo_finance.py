"""
Yahoo Finance Data Fetcher
Fetches stock data using yfinance API
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class StockDataFetcher:
    """Fetch stock data from Yahoo Finance API"""
    
    def __init__(self, ticker: str):
        """
        Initialize the stock data fetcher
        
        Args:
            ticker (str): Stock ticker symbol (e.g., 'AAPL', 'GOOGL', 'TSLA')
        """
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(self.ticker)
        
    def get_stock_info(self) -> Dict[str, Any]:
        """
        Get basic stock information
        
        Returns:
            dict: Stock information including name, sector, market cap, etc.
        """
        try:
            info = self.stock.info
            return {
                'symbol': self.ticker,
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'current_price': info.get('currentPrice', info.get('regularMarketPrice', 'N/A')),
                'previous_close': info.get('previousClose', 'N/A'),
                'volume': info.get('volume', 'N/A'),
                'average_volume': info.get('averageVolume', 'N/A'),
                '52_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
                '52_week_low': info.get('fiftyTwoWeekLow', 'N/A'),
            }
        except Exception as e:
            print(f"Error fetching stock info: {e}")
            return {}
    
    def get_historical_data(self, period: str = '1mo', interval: str = '1d') -> pd.DataFrame:
        """
        Get historical stock data
        
        Args:
            period (str): Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
            interval (str): Data interval ('1m', '5m', '15m', '1h', '1d', '1wk', '1mo')
        
        Returns:
            pd.DataFrame: Historical stock data with OHLCV (Open, High, Low, Close, Volume)
        """
        try:
            data = self.stock.history(period=period, interval=interval)
            if data.empty:
                print(f"No data found for {self.ticker}")
                return pd.DataFrame()
            return data
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return pd.DataFrame()
    
    def get_data_by_date_range(self, start_date: str, end_date: str, interval: str = '1d') -> pd.DataFrame:
        """
        Get historical data for a specific date range
        
        Args:
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format
            interval (str): Data interval ('1d', '1wk', '1mo')
        
        Returns:
            pd.DataFrame: Historical stock data
        """
        try:
            data = self.stock.history(start=start_date, end=end_date, interval=interval)
            if data.empty:
                print(f"No data found for {self.ticker} between {start_date} and {end_date}")
                return pd.DataFrame()
            return data
        except Exception as e:
            print(f"Error fetching data by date range: {e}")
            return pd.DataFrame()
    
    def get_daily_data(self, days: int = 30) -> pd.DataFrame:
        """
        Get daily stock data for the specified number of days
        
        Args:
            days (int): Number of days to fetch (default: 30)
        
        Returns:
            pd.DataFrame: Daily stock data
        """
        period_map = {
            5: '5d',
            7: '1mo',
            30: '1mo',
            90: '3mo',
            180: '6mo',
            365: '1y'
        }
        
        # Find closest period
        period = '1mo'
        for day_limit, p in sorted(period_map.items()):
            if days <= day_limit:
                period = p
                break
        if days > 365:
            period = 'max'
            
        return self.get_historical_data(period=period, interval='1d')
    
    def get_weekly_data(self, weeks: int = 12) -> pd.DataFrame:
        """
        Get weekly stock data
        
        Args:
            weeks (int): Number of weeks to fetch (default: 12)
        
        Returns:
            pd.DataFrame: Weekly stock data
        """
        if weeks <= 4:
            period = '1mo'
        elif weeks <= 12:
            period = '3mo'
        elif weeks <= 26:
            period = '6mo'
        else:
            period = '1y'
            
        return self.get_historical_data(period=period, interval='1wk')
    
    def calculate_price_change(self, data: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate price change statistics
        
        Args:
            data (pd.DataFrame): Stock data
        
        Returns:
            dict: Price change statistics (absolute, percentage, high, low)
        """
        if data.empty:
            return {}
        
        try:
            start_price = data['Close'].iloc[0]
            end_price = data['Close'].iloc[-1]
            highest_price = data['High'].max()
            lowest_price = data['Low'].min()
            
            change = end_price - start_price
            change_percent = (change / start_price) * 100
            
            return {
                'start_price': round(start_price, 2),
                'end_price': round(end_price, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'highest': round(highest_price, 2),
                'lowest': round(lowest_price, 2)
            }
        except Exception as e:
            print(f"Error calculating price change: {e}")
            return {}
    
    def get_current_price(self) -> Optional[float]:
        """
        Get the current/latest stock price
        
        Returns:
            float: Current price or None if unavailable
        """
        try:
            info = self.stock.info
            price = info.get('currentPrice', info.get('regularMarketPrice'))
            return price
        except Exception as e:
            print(f"Error fetching current price: {e}")
            return None
    
    def is_valid_ticker(self) -> bool:
        """
        Check if the ticker symbol is valid
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            info = self.stock.info
            return 'symbol' in info or 'longName' in info
        except:
            return False
