import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def display_game_summary(winner, start_time, stats):
    """
    Generates a high-visibility post-match analysis report using Rich.
    """
    duration = round(time.time() - start_time, 2)
    
    # Choose theme based on who won
    if winner == "player":
        banner_text = "[bold blink green]🎉🏆 CHAMPION REVEALED: YOU WIN! 🏆🎉[/bold blink green]"
        border_color = "green"
    else:
        banner_text = "[bold blink red]💀 CHAMPION REVEALED: COMPUTER WINS! 💀[/bold blink red]"
        border_color = "red"
        
    console.print("\n")
    console.print(Panel.fit(banner_text, border_style=border_color, padding=1))
    
    # Initialize the match facts matrix table
    summary_table = Table(title="[bold gold1]📋 UNO MATCH SUMMARY LOG[/bold gold1]", show_lines=True, header_style="bold cyan")
    
    summary_table.add_column("Metric Description", style="dim white", width=30)
    summary_table.add_column("Player (You)", justify="center", style="green")
    summary_table.add_column("Computer (AI)", justify="center", style="magenta")
    
    # Add comparative tracking items
    summary_table.add_row("Final Cards Remaining", str(stats["player_final_cards"]), str(stats["computer_final_cards"]))
    summary_table.add_row("Total Cards Played", str(stats["player_cards_played"]), str(stats["computer_cards_played"]))
    summary_table.add_row("Total Cards Drawn", str(stats["player_cards_drawn"]), str(stats["computer_cards_drawn"]))
    summary_table.add_row("Wild Cards Triggered", str(stats["player_wilds"]), str(stats["computer_wilds"]))
    
    console.print(summary_table)
    
    # Sub-footer showing chronological data
    console.print(Panel(f"[bold white]⏱️ Match Session Duration:[/bold white] [yellow]{duration} seconds[/yellow]", border_style="cyan", expand=False))