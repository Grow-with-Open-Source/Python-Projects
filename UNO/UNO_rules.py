# define game rules to follow     
def check_rules_for_cards(card,previous_card):
    
    # check and return true and false    
    
    wild_cards = ['wild', 'wild_draw_four']

    if card['color'] == previous_card['color']:
        return True

    if card['value'] == previous_card['value']:
        return True

    if card['value'] in wild_cards:
        return True

    return False


def apply_power_card(card, current_player,
                     player_hand,
                     computer_hand,
                     deck):

    value = card['value']

    if value == 'draw_two':

        if current_player == 'player':
            for _ in range(2):
                computer_hand.append(deck.pop())

        else:
            for _ in range(2):
                player_hand.append(deck.pop())

        return "skip"

    elif value == 'skip':
        return "skip"

    elif value == 'reverse':
        return "skip"  # reverse == skip for 2 players

    elif value == 'wild_draw_four':

        if current_player == 'player':
            for _ in range(4):
                computer_hand.append(deck.pop())

        else:
            for _ in range(4):
                player_hand.append(deck.pop())

        return "skip"

    elif value == 'wild':
        return "wild"

    return None
