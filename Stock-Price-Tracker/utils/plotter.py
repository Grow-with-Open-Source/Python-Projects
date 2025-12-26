"""
Stock Price Plotter
Creates various charts and visualizations for stock data
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from typing import Optional


class StockPlotter:
    """Create visualizations for stock data"""
    
    def __init__(self, ticker: str):
        """
        Initialize the stock plotter
        
        Args:
            ticker (str): Stock ticker symbol
        """
        self.ticker = ticker.upper()
    
    def plot_price_trend(self, data: pd.DataFrame, title: str = None, 
                        save_path: Optional[str] = None, show_plot: bool = True):
        """
        Plot stock price trend using matplotlib
        
        Args:
            data (pd.DataFrame): Stock data with 'Close' column
            title (str): Plot title
            save_path (str): Path to save the plot
            show_plot (bool): Whether to display the plot
        """
        if data.empty:
            print("No data to plot")
            return
        
        plt.figure(figsize=(14, 7))
        
        # Plot closing price
        plt.plot(data.index, data['Close'], label='Close Price', 
                color='#2E86C1', linewidth=2)
        
        # Add moving averages
        if len(data) >= 7:
            ma7 = data['Close'].rolling(window=7).mean()
            plt.plot(data.index, ma7, label='7-Day MA', 
                    color='#E67E22', linestyle='--', linewidth=1.5)
        
        if len(data) >= 30:
            ma30 = data['Close'].rolling(window=30).mean()
            plt.plot(data.index, ma30, label='30-Day MA', 
                    color='#27AE60', linestyle='--', linewidth=1.5)
        
        # Formatting
        if title is None:
            title = f'{self.ticker} Stock Price Trend'
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Date', fontsize=12, fontweight='bold')
        plt.ylabel('Price ($)', fontsize=12, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Format x-axis
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gcf().autofmt_xdate()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        if show_plot:
            plt.show()
        else:
            plt.close()
    
    def plot_candlestick(self, data: pd.DataFrame, title: str = None,
                        save_path: Optional[str] = None, show_plot: bool = True):
        """
        Create interactive candlestick chart using plotly
        
        Args:
            data (pd.DataFrame): Stock data with OHLC columns
            title (str): Chart title
            save_path (str): Path to save the chart
            show_plot (bool): Whether to display the chart
        """
        if data.empty:
            print("No data to plot")
            return
        
        # Create figure with secondary y-axis
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.7, 0.3],
            subplot_titles=(f'{self.ticker} Price', 'Volume')
        )
        
        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='OHLC',
                increasing_line_color='#26A69A',
                decreasing_line_color='#EF5350'
            ),
            row=1, col=1
        )
        
        # Volume bar chart
        colors = ['#26A69A' if close >= open else '#EF5350' 
                 for close, open in zip(data['Close'], data['Open'])]
        
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume',
                marker_color=colors,
                showlegend=False
            ),
            row=2, col=1
        )
        
        # Update layout
        if title is None:
            title = f'{self.ticker} Candlestick Chart'
        
        fig.update_layout(
            title=title,
            title_font_size=18,
            xaxis_rangeslider_visible=False,
            height=700,
            template='plotly_white',
            hovermode='x unified'
        )
        
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        
        if save_path:
            fig.write_html(save_path)
            print(f"Interactive chart saved to {save_path}")
        
        if show_plot:
            fig.show()
    
    def plot_volume_analysis(self, data: pd.DataFrame, title: str = None,
                           save_path: Optional[str] = None, show_plot: bool = True):
        """
        Plot volume analysis
        
        Args:
            data (pd.DataFrame): Stock data with Volume column
            title (str): Plot title
            save_path (str): Path to save the plot
            show_plot (bool): Whether to display the plot
        """
        if data.empty:
            print("No data to plot")
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), 
                                       height_ratios=[2, 1], sharex=True)
        
        # Price subplot
        ax1.plot(data.index, data['Close'], label='Close Price', 
                color='#2E86C1', linewidth=2)
        ax1.set_ylabel('Price ($)', fontsize=12, fontweight='bold')
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        
        # Volume subplot
        colors = ['#26A69A' if close >= open else '#EF5350' 
                 for close, open in zip(data['Close'], data['Open'])]
        ax2.bar(data.index, data['Volume'], color=colors, alpha=0.7)
        ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Volume', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add average volume line
        avg_volume = data['Volume'].mean()
        ax2.axhline(y=avg_volume, color='orange', linestyle='--', 
                   linewidth=2, label=f'Avg Volume: {avg_volume:,.0f}')
        ax2.legend(loc='best')
        
        if title is None:
            title = f'{self.ticker} Price & Volume Analysis'
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Volume analysis plot saved to {save_path}")
        
        if show_plot:
            plt.show()
        else:
            plt.close()
    
    def plot_comparison(self, data: pd.DataFrame, comparison_type: str = 'daily',
                       save_path: Optional[str] = None, show_plot: bool = True):
        """
        Create comparison plots (daily vs weekly)
        
        Args:
            data (pd.DataFrame): Stock data
            comparison_type (str): Type of comparison ('daily' or 'weekly')
            save_path (str): Path to save the plot
            show_plot (bool): Whether to display the plot
        """
        if data.empty:
            print("No data to plot")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle(f'{self.ticker} Stock Analysis - {comparison_type.capitalize()}', 
                    fontsize=16, fontweight='bold')
        
        # Price trend
        axes[0, 0].plot(data.index, data['Close'], color='#2E86C1', linewidth=2)
        axes[0, 0].set_title('Closing Price', fontweight='bold')
        axes[0, 0].set_ylabel('Price ($)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Volume
        axes[0, 1].bar(data.index, data['Volume'], color='#3498DB', alpha=0.7)
        axes[0, 1].set_title('Trading Volume', fontweight='bold')
        axes[0, 1].set_ylabel('Volume')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Daily returns
        returns = data['Close'].pct_change() * 100
        axes[1, 0].plot(data.index, returns, color='#27AE60', linewidth=1.5)
        axes[1, 0].axhline(y=0, color='red', linestyle='--', linewidth=1)
        axes[1, 0].set_title('Daily Returns (%)', fontweight='bold')
        axes[1, 0].set_ylabel('Return (%)')
        axes[1, 0].set_xlabel('Date')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Price distribution
        axes[1, 1].hist(data['Close'], bins=30, color='#E67E22', alpha=0.7, edgecolor='black')
        axes[1, 1].set_title('Price Distribution', fontweight='bold')
        axes[1, 1].set_xlabel('Price ($)')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Comparison plot saved to {save_path}")
        
        if show_plot:
            plt.show()
        else:
            plt.close()
    
    def create_summary_report(self, data: pd.DataFrame, stats: dict,
                            save_path: Optional[str] = None, show_plot: bool = True):
        """
        Create a comprehensive visual summary report
        
        Args:
            data (pd.DataFrame): Stock data
            stats (dict): Price change statistics
            save_path (str): Path to save the report
            show_plot (bool): Whether to display the report
        """
        if data.empty or not stats:
            print("Insufficient data for summary report")
            return
        
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # Title
        fig.suptitle(f'{self.ticker} Stock Analysis Report', 
                    fontsize=18, fontweight='bold', y=0.98)
        
        # Main price chart
        ax1 = fig.add_subplot(gs[0:2, :])
        ax1.plot(data.index, data['Close'], label='Close Price', 
                color='#2E86C1', linewidth=2.5)
        ax1.fill_between(data.index, data['Low'], data['High'], 
                        alpha=0.2, color='#85C1E9', label='Daily Range')
        ax1.set_title('Price Trend with Daily Range', fontweight='bold', fontsize=14)
        ax1.set_ylabel('Price ($)', fontsize=12)
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        
        # Statistics text box
        ax2 = fig.add_subplot(gs[2, 0])
        ax2.axis('off')
        stats_text = f"""
        STATISTICS SUMMARY
        ━━━━━━━━━━━━━━━━━━━━━━━━━
        Start Price:    ${stats.get('start_price', 'N/A')}
        End Price:      ${stats.get('end_price', 'N/A')}
        Change:         ${stats.get('change', 'N/A')} ({stats.get('change_percent', 'N/A')}%)
        Highest:        ${stats.get('highest', 'N/A')}
        Lowest:         ${stats.get('lowest', 'N/A')}
        Range:          ${stats.get('highest', 0) - stats.get('lowest', 0):.2f}
        """
        ax2.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                verticalalignment='center', bbox=dict(boxstyle='round', 
                facecolor='wheat', alpha=0.5))
        
        # Volume chart
        ax3 = fig.add_subplot(gs[2, 1])
        ax3.bar(data.index, data['Volume'], color='#3498DB', alpha=0.6)
        ax3.set_title('Trading Volume', fontweight='bold', fontsize=12)
        ax3.set_ylabel('Volume', fontsize=10)
        ax3.grid(True, alpha=0.3, axis='y')
        ax3.tick_params(axis='x', rotation=45)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Summary report saved to {save_path}")
        
        if show_plot:
            plt.show()
        else:
            plt.close()
