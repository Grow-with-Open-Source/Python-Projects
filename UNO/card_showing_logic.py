import random 

def get_discard(deck):
    """retruns the fair uno start card so that no power card on start """    
    action_cards = ['skip', 'reverse', 'draw_two','wild_draw_four','wild','wild_six']

    while True:
        
        selected_card = random.choice(deck)
        
        if selected_card['value'] not in action_cards:
            deck.remove(selected_card)
            return selected_card

        
def get_dicard_card(deck):
    
    discard_card = get_discard(deck)

    discard_card_layout = f"""
    =========================
    |         DC          
    | Color : {discard_card['color']}
    | Value : {discard_card['value']}
    =========================
    """
    
    return discard_card

def show_players_cards(player_hand):
    
    for i , card in enumerate(player_hand):
        player_card = f'''
        ========================
        |        {i+1}         
        |Color : {card['color']}
        |Value : {card['value']}
        ========================
        '''
        print(player_card,end=' ')




