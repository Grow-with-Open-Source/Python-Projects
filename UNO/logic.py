from time import time
import numpy as np
import random
from deck import get_deck
from card_showing_logic import get_dicard_card , show_players_cards , show_player_selcted_card,show_computer_selcted_card
from UNO_rules import check_rules_for_cards , apply_power_card


class UNO:
    
    def __init__(self,n_players=2,ncards=108):
       self.n_players = n_players
       self.ncards = ncards
           
    def start_game(self):
        #all displaying things 
        # game logic 
        # first shuffle then draw hands of cards  
        
        deck = get_deck(self.ncards)
        deck = self._shuffle(deck)
        hands = self._draw_players_cards(deck=deck,players=self.n_players)
        
        player_hand = hands['player']
        computer_hand = hands['computer']

        dicard_card = get_dicard_card(deck=deck) #display the discard card
        
        used_cards = []
        used_cards.append(dicard_card)
        
        print('player cards....')
        
        show_players_cards(player_hand=player_hand) # displayes the player cards on screen 
        
        current_player = 'player'
        
        while player_hand and computer_hand:
            
            previous_card = used_cards[-1]
            
            # game logic to and fro
            if current_player == 'player':
                print('player turn')
                
                while True:
                    # check if user have cards or not 
                    have_cards = input('entre Y is have entre N if not ').upper()
                    get_display = input('entre show if you wanna see your cards ').lower()
                    
                    if get_display == 'show':
                        show_players_cards(player_hand)
                        
                    if have_cards == 'Y':
                        # get user card 
                        
                        card_num = int(input('entre the card number to play : please note 1 is 0 and so on  '))
                        
                        if card_num >= len(player_hand) or card_num < 0:
                            print("Invalid index")
                            continue
                        
                        current_card = player_hand[card_num]
                        
                    
                        if check_rules_for_cards(current_card,previous_card):
                            
                            if card_num < len(player_hand): # must be within range
                                player_used_card = player_hand.pop(card_num)
                                used_cards.append(player_used_card)
                                
                                effect = apply_power_card(
                                    player_used_card,
                                    current_player,
                                    player_hand,
                                    computer_hand,
                                    deck
                                )
                                
                            else:
                                print('sussy boi play vaild ....')
                                
                            print('$'*20)
                            print('now player have these cards')
                            
                            show_players_cards(player_hand=player_hand)
                            
                            print('$'*20)
                            show_player_selcted_card(player_used_card)
                    
                            if effect == "skip":
                                print("Computer loses turn")
                                current_player = "player"
                                
                            else:
                                current_player = "computer"
                                break   
            
                            if len(player_hand) == 1:
                                print("UNO!")
                                
                            break 
                        else:
                            print('INVALID card try again !!')           
                    else:
                        print('player draw a card')
                        
                        drawn_card = deck.pop()
                        player_hand.append(drawn_card)
                        
                        if effect == "skip":
                            print("Computer loses turn")
                            current_player = "player"
                        else:
                            current_player = "computer"
                        break   
            
            else:
                played = False
                
                print('$'*20)
                print('computer turn ')
                
                for i, card in enumerate(computer_hand):

                    if check_rules_for_cards(card, previous_card):
                        
                        played_card = computer_hand.pop(i)
                        show_computer_selcted_card(played_card)
                        used_cards.append(played_card)
                        
                        effect = apply_power_card(
                                played_card,
                                current_player,
                                player_hand,
                                computer_hand,
                                deck
                            )
                        
                        if len(player_hand) == 1:
                               print("UNO!")
                               
                        played = True
                        break
                    
                if not played:

                    print("Computer draws a card")

                    drawn_card = deck.pop()
                    computer_hand.append(drawn_card)

                if effect == "skip":
                    print("Player loses turn")
                    current_player = "computer"
                else:
                    current_player = "player"
                
        if len(player_hand) == 0:
            print("🎉 PLAYER WINS!")
            return

        if len(computer_hand) == 0:
            print("💀 COMPUTER WINS!")
            return

                

    def _shuffle(self,deck):
        random.shuffle(deck)
        return deck
    
    def _draw_players_cards(self,deck,players=2):
        hands = {
            'player':[],
            'computer':[]
        }

        for _ in range(7):
            hands['player'].append(deck.pop())
            hands['computer'].append(deck.pop())

        return hands

game = UNO()
game.start_game()