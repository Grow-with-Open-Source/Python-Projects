import random
import time
import numpy as np

from deck import get_deck
from card_showing_logic import get_dicard_card, show_players_cards
from UNO_rules import check_rules_for_cards , apply_power_card

from summary import display_game_summary

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns

console = Console()

class UNO:
    
    def __init__(self, n_players=2, ncards=108):
        self.n_players = n_players
        self.ncards = ncards
        
        self.stats = {
            "player_cards_played": 0,
            "computer_cards_played": 0,
            "player_cards_drawn": 0,
            "computer_cards_drawn": 0,
            "player_wilds": 0,
            "computer_wilds": 0,
            "player_final_cards": 0,
            "computer_final_cards": 0
        }
            
    def start_game(self):
        start_time = time.time()  # Start session timer clock
        
        deck = get_deck(self.ncards)
        deck = self._shuffle(deck)
        hands = self._draw_players_cards(deck=deck, players=self.n_players)
        
        player_hand = hands['player']
        computer_hand = hands['computer']

        discard_card = get_dicard_card(deck=deck) 
        used_cards = []
        used_cards.append(discard_card)
        
        # Track dynamically selected target card or overridden active color string
        declared_wild_color = None
        
        console.print(Panel.fit("[bold blink yellow]🔥 WELCOME TO UNO 🔥[/bold blink yellow]", border_style="magenta"))
        current_player = 'player'
        
        while player_hand and computer_hand:
            previous_card = used_cards[-1]
            effect = None  
            
            # Formulate current target display based on whether a wild choice is overriding the card
            if declared_wild_color:
                display_color_status = f"[bold magenta]{previous_card}[/bold magenta] -> [bold yellow]Active Color: {declared_wild_color.upper()}[/bold yellow]"
            else:
                display_color_status = str(previous_card)

            # Visual State Dashboard
            console.print("\n" + "─" * 60, style="dim white")
            board_table = Table(title="[bold cyan]CURRENT GAME STATE[/bold cyan]", show_header=False, box=None)
            board_table.add_row("[bold]Top Discard Pile Card:[/bold]", f"[bold reverse] {display_color_status} [/bold reverse]")
            board_table.add_row("[bold]Computer Cards Left:[/bold]", f"[bold red]{len(computer_hand)}[/bold red] 🎴")
            console.print(Panel(board_table, border_style="cyan"))

            # ---------------- REGULAR PLAYER TURN ----------------
            if current_player == 'player':
                console.print("[bold green]👉 YOUR TURN[/bold green]")
                console.print('\n[bold underline green]Your Current Hand:[/bold underline green]')
                
                # Render hand layout dynamically matching colors
                cards_render = []
                for i, card_obj in enumerate(player_hand):
                    card_str = str(card_obj).lower()
                    border_color = "white"
                    if "red" in card_str: border_color = "red"
                    elif "blue" in card_str: border_color = "blue"
                    elif "green" in card_str: border_color = "green"
                    elif "yellow" in card_str: border_color = "yellow"
                    elif "wild" in card_str: border_color = "magenta"
                    
                    cards_render.append(Panel(f"[bold]{card_obj}[/bold]", title=f"[bold yellow][{i}][/bold yellow]", border_style=border_color))
                
                console.print(Columns(cards_render))
                print("") 
                
                while True:
                    have_cards = console.input("[bold yellow]Do you have a playable card? (Y/N): [/bold yellow]").upper().strip()
                    
                    if have_cards == 'Y':
                        try:
                            card_num = int(console.input('Enter the index number of the card you want to play: '))
                        except ValueError:
                            console.print("[bold red]Please enter a valid integer choice.[/bold red]")
                            continue
                        
                        if card_num >= len(player_hand) or card_num < 0:
                            console.print("[bold red]Invalid index! Choice out of bounds.[/bold red]")
                            continue
                        
                        current_card = player_hand[card_num]
                        
                        # Validate choice factoring in active wild overrides
                        is_valid_move = False
                        if "wild" in str(current_card).lower():
                            is_valid_move = True  # Wilds are always playable
                        elif declared_wild_color:
                            # Must match overridden color choice declaration
                            is_valid_move = (declared_wild_color.lower() in str(current_card).lower())
                        else:
                            is_valid_move = check_rules_for_cards(current_card, previous_card)
                        
                        if is_valid_move:
                            player_used_card = player_hand.pop(card_num)
                            used_cards.append(player_used_card)
                            self.stats["player_cards_played"] += 1
                            
                            # Handle Wild declaration prompt interaction
                            if "wild" in str(player_used_card).lower():
                                self.stats["player_wilds"] += 1
                                while True:
                                    choice = console.input("[bold magenta]🌈 WILD PLAYED! Choose active color (Red/Blue/Green/Yellow): [/bold magenta]").strip().lower()
                                    if choice in ["red", "blue", "green", "yellow"]:
                                        declared_wild_color = choice
                                        break
                                    console.print("[bold red]Invalid color selection. Try again.[/bold red]")
                            else:
                                # Regular card placement clears out old active wild overrides
                                declared_wild_color = None

                            if len(player_hand) == 1:
                                console.print(Panel("[bold blink red]📣 UNO! YOU HAVE ONLY ONE CARD LEFT![/bold blink red]", border_style="red"))

                            effect = apply_power_card(player_used_card, current_player, player_hand, computer_hand, deck)
                                
                            console.print("\n" + "[bold gold1]$" * 20 + " ACTION CONFIRMED " + "$" * 20 + "[/bold gold1]")
                            
                            if effect == "skip":
                                console.print("[bold orange3]🚫 Computer loses its turn! You get another go.[/bold orange3]")
                                current_player = "player"
                            else:
                                current_player = "computer"
                            break 
                        else:
                            console.print('[bold red]❌ INVALID CARD! Match color criteria or drop a Wild.[/bold red]')           
                    else:
                        console.print('[bold orange1]📥 Drawing a card from the deck...[/bold orange1]')
                        if len(deck) == 0:
                            deck = self._shuffle(used_cards[:-1])
                            used_cards = [used_cards[-1]]
                        
                        drawn_card = deck.pop()
                        player_hand.append(drawn_card)
                        self.stats["player_cards_drawn"] += 1
                        
                        console.print(f"You drew: [bold reverse] {drawn_card} [/bold reverse]")
                        
                        if effect == "skip":
                            console.print("[bold orange3]🚫 Computer loses its turn.[/bold orange3]")
                            current_player = "player"
                        else:
                            current_player = "computer"
                        break   
            
            # ---------------- COMPUTER TURN ----------------
            else:
                played = False
                console.print('\n[bold magenta]🤖 COMPUTER\'S TURN[/bold magenta]')
                time.sleep(0.8)  # Imparts an interactive human thinking buffer
                
                for i, card in enumerate(computer_hand):
                    is_valid_move = False
                    if "wild" in str(card).lower():
                        is_valid_move = True
                    elif declared_wild_color:
                        is_valid_move = (declared_wild_color.lower() in str(card).lower())
                    else:
                        is_valid_move = check_rules_for_cards(card, previous_card)
                        
                    if is_valid_move:
                        played_card = computer_hand.pop(i)
                        used_cards.append(played_card)
                        self.stats["computer_cards_played"] += 1
                        
                        # AI Wild processing rule
                        if "wild" in str(played_card).lower():
                            self.stats["computer_wilds"] += 1
                            # Simple smart feature: AI looks at its own hand to match its most frequent color
                            hand_colors = [c for c in ["red", "blue", "green", "yellow"] if c in str(computer_hand).lower()]
                            declared_wild_color = random.choice(hand_colors) if hand_colors else random.choice(["red", "blue", "green", "yellow"])
                            console.print(f"[bold magenta]🤖 AI played a Wild Card and declared the new active color as: {declared_wild_color.upper()}[/bold magenta]")
                        else:
                            declared_wild_color = None

                        if len(computer_hand) == 1:
                            console.print(Panel("[bold blink red]🤖 COMPUTER SHOUTS: UNO![/bold blink red]", border_style="red"))
                            
                        console.print(f"Computer laid down: [bold reverse] {played_card} [/bold reverse]")
                        
                        effect = apply_power_card(played_card, current_player, player_hand, computer_hand, deck)
                        played = True
                        break
                    
                if not played:
                    console.print("[bold dim orange1]Computer couldn't play. Drawing a card...[/bold dim orange1]")
                    if len(deck) == 0:
                        deck = self._shuffle(used_cards[:-1])
                        used_cards = [used_cards[-1]]
                    drawn_card = deck.pop()
                    computer_hand.append(drawn_card)
                    self.stats["computer_cards_drawn"] += 1

                if effect == "skip":
                    console.print("[bold orange3]🚫 Player loses turn! AI goes again.[/bold orange3]")
                    current_player = "computer"
                else:
                    current_player = "player"
                
        # --- GAME END STATE EVALUATION GENERATOR ---
        self.stats["player_final_cards"] = len(player_hand)
        self.stats["computer_final_cards"] = len(computer_hand)
        
        winner_declared = "player" if len(player_hand) == 0 else "computer"
        
        # Fire external execution wrap summary module
        display_game_summary(winner_declared, start_time, self.stats)

    def _shuffle(self, deck):
        random.shuffle(deck)
        return deck
    
    def _draw_players_cards(self, deck, players=2):
        hands = {'player': [], 'computer': []}
        for _ in range(7):
            hands['player'].append(deck.pop())
            hands['computer'].append(deck.pop())
        return hands
