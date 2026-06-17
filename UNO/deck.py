import random

def get_deck(N=108):
    """
    Generates an Uno deck.

    N = 108 -> Standard UNO deck
    N = 112 -> Standard deck + 4 extra customizable wild cards
    """

    deck = []

    colors = ['blue', 'red', 'green', 'yellow']
    action_cards = ['skip', 'reverse', 'draw_two']

    # Number cards
    for color in colors:
        # One 0 per color
        deck.append({"color": color, "value": "0"})

        # Two of each 1-9 per color
        for num in range(1, 10):
            deck.append({"color": color, "value": str(num)})
            deck.append({"color": color, "value": str(num)})

    # Action cards
    for color in colors:
        for action in action_cards:
            deck.append({"color": color, "value": action})
            deck.append({"color": color, "value": action})

    # Wild cards
    for _ in range(4):
        deck.append({"color": "black", "value": "wild"})
        deck.append({"color": "black", "value": "wild_draw_four"})

    if N == 112:
        for _ in range(4):
            deck.append({"color": "black", "value": "wild_six"})

    return deck