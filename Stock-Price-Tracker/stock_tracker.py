#!/usr/bin/env python3
"""
Stock Price Tracker
Track stock prices, visualize trends, and send Telegram alerts

Author: Python-Projects Contributors
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.yahoo_finance import StockDataFetcher
from utils.plotter import StockPlotter
from utils.telegram_alert import TelegramAlert


class StockTracker:
    """Main Stock Price Tracker Application"""
    
    def __init__(self, ticker: str, use_telegram: bool = False):
        """
        Initialize Stock Tracker
        
        Args:
            ticker (str): Stock ticker symbol
            use_telegram (bool): Enable Telegram alerts
        """
        self.ticker = ticker.upper()
        self.fetcher = StockDataFetcher(self.ticker)
        self.plotter = StockPlotter(self.ticker)
        self.telegram = TelegramAlert() if use_telegram else None
        
    def validate_ticker(self) -> bool:
        """Validate if ticker symbol is valid"""
        print(f"🔍 Validating ticker symbol: {self.ticker}")
        if self.fetcher.is_valid_ticker():
            print(f"✅ Ticker {self.ticker} is valid")
            return True
        else:
            print(f"❌ Invalid ticker symbol: {self.ticker}")
            return False
    
    def display_stock_info(self):
        """Display basic stock information"""
        print(f"\n{'='*60}")
        print(f"📊 STOCK INFORMATION: {self.ticker}")
        print(f"{'='*60}")
        
        info = self.fetcher.get_stock_info()
        if info:
            print(f"Company:        {info.get('name', 'N/A')}")
            print(f"Sector:         {info.get('sector', 'N/A')}")
            print(f"Industry:       {info.get('industry', 'N/A')}")
            print(f"Current Price:  ${info.get('current_price', 'N/A')}")
            print(f"Previous Close: ${info.get('previous_close', 'N/A')}")
            print(f"52W High:       ${info.get('52_week_high', 'N/A')}")
            print(f"52W Low:        ${info.get('52_week_low', 'N/A')}")
            
            if isinstance(info.get('market_cap'), (int, float)):
                market_cap_b = info['market_cap'] / 1e9
                print(f"Market Cap:     ${market_cap_b:.2f}B")
            print(f"{'='*60}\n")
        else:
            print("❌ Unable to fetch stock information\n")
    
    def track_daily(self, days: int = 30, plot: bool = True, 
                   save_plots: bool = False, send_alert: bool = False):
        """
        Track daily stock prices
        
        Args:
            days (int): Number of days to track
            plot (bool): Display plots
            save_plots (bool): Save plots to files
            send_alert (bool): Send Telegram alert
        """
        print(f"\n📈 Fetching {days} days of data for {self.ticker}...")
        data = self.fetcher.get_daily_data(days)
        
        if data.empty:
            print("❌ No data available")
            return
        
        print(f"✅ Retrieved {len(data)} days of data")
        
        # Calculate statistics
        stats = self.fetcher.calculate_price_change(data)
        
        # Display statistics
        self._display_statistics(stats, "Daily")
        
        # Create plots
        if plot or save_plots:
            self._create_plots(data, stats, "daily", plot, save_plots)
        
        # Send Telegram alert
        if send_alert and self.telegram and self.telegram.is_configured():
            print("\n📱 Sending Telegram alert...")
            success = self.telegram.send_stock_alert(self.ticker, stats, "daily_summary")
            if success:
                print("✅ Alert sent successfully")
            else:
                print("❌ Failed to send alert")
    
    def track_weekly(self, weeks: int = 12, plot: bool = True,
                    save_plots: bool = False, send_alert: bool = False):
        """
        Track weekly stock prices
        
        Args:
            weeks (int): Number of weeks to track
            plot (bool): Display plots
            save_plots (bool): Save plots to files
            send_alert (bool): Send Telegram alert
        """
        print(f"\n📊 Fetching {weeks} weeks of data for {self.ticker}...")
        data = self.fetcher.get_weekly_data(weeks)
        
        if data.empty:
            print("❌ No data available")
            return
        
        print(f"✅ Retrieved {len(data)} weeks of data")
        
        # Calculate statistics
        stats = self.fetcher.calculate_price_change(data)
        
        # Display statistics
        self._display_statistics(stats, "Weekly")
        
        # Create plots
        if plot or save_plots:
            self._create_plots(data, stats, "weekly", plot, save_plots)
        
        # Send Telegram alert
        if send_alert and self.telegram and self.telegram.is_configured():
            print("\n📱 Sending Telegram alert...")
            success = self.telegram.send_stock_alert(self.ticker, stats, "update")
            if success:
                print("✅ Alert sent successfully")
            else:
                print("❌ Failed to send alert")
    
    def check_price_threshold(self, threshold: float, threshold_type: str = "above"):
        """
        Check if current price crosses a threshold
        
        Args:
            threshold (float): Price threshold
            threshold_type (str): 'above' or 'below'
        """
        print(f"\n🎯 Checking price threshold...")
        current_price = self.fetcher.get_current_price()
        
        if current_price is None:
            print("❌ Unable to fetch current price")
            return
        
        print(f"Current Price: ${current_price:.2f}")
        print(f"Threshold: ${threshold:.2f} ({threshold_type})")
        
        triggered = False
        if threshold_type == "above" and current_price > threshold:
            triggered = True
            print(f"✅ Price is above threshold!")
        elif threshold_type == "below" and current_price < threshold:
            triggered = True
            print(f"✅ Price is below threshold!")
        else:
            print(f"ℹ️  Threshold not triggered")
        
        if triggered and self.telegram and self.telegram.is_configured():
            print("\n📱 Sending threshold alert...")
            success = self.telegram.send_price_threshold_alert(
                self.ticker, current_price, threshold, threshold_type
            )
            if success:
                print("✅ Alert sent successfully")
    
    def _display_statistics(self, stats: dict, timeframe: str):
        """Display price change statistics"""
        print(f"\n{'─'*60}")
        print(f"📊 {timeframe.upper()} STATISTICS")
        print(f"{'─'*60}")
        print(f"Start Price:  ${stats.get('start_price', 'N/A')}")
        print(f"End Price:    ${stats.get('end_price', 'N/A')}")
        print(f"Change:       ${stats.get('change', 'N/A')} ({stats.get('change_percent', 'N/A')}%)")
        print(f"Highest:      ${stats.get('highest', 'N/A')}")
        print(f"Lowest:       ${stats.get('lowest', 'N/A')}")
        print(f"{'─'*60}\n")
    
    def _create_plots(self, data, stats, timeframe: str, 
                     show: bool, save: bool):
        """Create and save plots"""
        assets_dir = Path(__file__).parent / "assets" / "img"
        assets_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Price trend plot
        print(f"📊 Creating price trend plot...")
        save_path = None
        if save:
            save_path = str(assets_dir / f"{self.ticker}_{timeframe}_trend_{timestamp}.png")
        
        self.plotter.plot_price_trend(
            data, 
            title=f"{self.ticker} {timeframe.capitalize()} Price Trend",
            save_path=save_path,
            show_plot=show
        )
        
        # Candlestick chart (only for daily data with OHLC)
        if timeframe == "daily" and len(data) > 0:
            print(f"📊 Creating candlestick chart...")
            save_path = None
            if save:
                save_path = str(assets_dir / f"{self.ticker}_candlestick_{timestamp}.html")
            
            self.plotter.plot_candlestick(
                data,
                save_path=save_path,
                show_plot=show
            )
        
        # Summary report
        print(f"📊 Creating summary report...")
        save_path = None
        if save:
            save_path = str(assets_dir / f"{self.ticker}_summary_{timestamp}.png")
        
        self.plotter.create_summary_report(
            data, stats,
            save_path=save_path,
            show_plot=show
        )


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Stock Price Tracker - Track stocks, visualize trends, send alerts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Track daily prices for Apple
  python stock_tracker.py AAPL --daily

  # Track weekly prices for Google with plots
  python stock_tracker.py GOOGL --weekly --plot

  # Track with Telegram alerts
  python stock_tracker.py TSLA --daily --telegram --alert

  # Save plots without displaying
  python stock_tracker.py MSFT --daily --save-plots --no-plot

  # Check price threshold
  python stock_tracker.py AAPL --threshold 150 --threshold-type above --telegram
        """
    )
    
    parser.add_argument('ticker', type=str, help='Stock ticker symbol (e.g., AAPL, GOOGL, TSLA)')
    parser.add_argument('--daily', action='store_true', help='Track daily prices')
    parser.add_argument('--weekly', action='store_true', help='Track weekly prices')
    parser.add_argument('--days', type=int, default=30, help='Number of days to track (default: 30)')
    parser.add_argument('--weeks', type=int, default=12, help='Number of weeks to track (default: 12)')
    parser.add_argument('--plot', action='store_true', default=True, help='Display plots (default: True)')
    parser.add_argument('--no-plot', action='store_true', help='Do not display plots')
    parser.add_argument('--save-plots', action='store_true', help='Save plots to files')
    parser.add_argument('--telegram', action='store_true', help='Enable Telegram alerts')
    parser.add_argument('--alert', action='store_true', help='Send Telegram alert')
    parser.add_argument('--threshold', type=float, help='Price threshold for alerts')
    parser.add_argument('--threshold-type', choices=['above', 'below'], default='above',
                       help='Threshold type (default: above)')
    parser.add_argument('--info', action='store_true', help='Display stock information only')
    
    args = parser.parse_args()
    
    # Load environment variables
    env_path = Path(__file__).parent / 'config' / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    # Display header
    print("\n" + "="*60)
    print("📈 STOCK PRICE TRACKER")
    print("="*60)
    
    # Initialize tracker
    tracker = StockTracker(args.ticker, use_telegram=args.telegram)
    
    # Validate ticker
    if not tracker.validate_ticker():
        sys.exit(1)
    
    # Test Telegram connection if enabled
    if args.telegram:
        print("\n📱 Testing Telegram connection...")
        if tracker.telegram and tracker.telegram.test_connection():
            tracker.telegram.send_welcome_message(args.ticker)
        else:
            print("⚠️  Telegram not configured properly. Continuing without alerts.")
    
    # Display stock info
    if args.info:
        tracker.display_stock_info()
        return
    
    # Check threshold
    if args.threshold is not None:
        tracker.check_price_threshold(args.threshold, args.threshold_type)
        return
    
    # Determine plot settings
    show_plots = args.plot and not args.no_plot
    
    # Track prices
    if args.weekly:
        tracker.track_weekly(
            weeks=args.weeks,
            plot=show_plots,
            save_plots=args.save_plots,
            send_alert=args.alert
        )
    elif args.daily or (not args.daily and not args.weekly):
        # Default to daily if neither specified
        tracker.track_daily(
            days=args.days,
            plot=show_plots,
            save_plots=args.save_plots,
            send_alert=args.alert
        )
    
    print("\n✅ Stock tracking complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
