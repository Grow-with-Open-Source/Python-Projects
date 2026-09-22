#!/usr/bin/env python3
"""
main.py
A simple Rock Paper Scissors game against the computer.
The player picks rock, paper, or scissors and plays against a random computer choice.
"""

import random


def get_winner(player: str, computer: str) -> str:
    """Return 'player', 'computer', or 'tie' based on the two choices."""
    if player == computer:
        return "tie"
    if (player == "rock" and computer == "scissors") or \
       (player == "paper" and computer == "rock") or \
       (player == "scissors" and computer == "paper"):
        return "player"
    return "computer"


def main() -> None:
    """Run the game loop."""
    choices = ["rock", "paper", "scissors"]
    player_score = 0
    computer_score = 0

    print("Rock Paper Scissors")
    print("--------------------")
    print("Type 'quit' to exit.\n")

    while True:
        player_input = input("Choose rock, paper, or scissors: ").strip().lower()

        if player_input == "quit":
            print("\nThanks for playing!")
            print(f"Final score: You {player_score} - {computer_score} Computer")
            break

        if player_input not in choices:
            print("Invalid choice. Try again.\n")
            continue

        computer_choice = random.choice(choices)
        print(f"Computer chose: {computer_choice}")

        result = get_winner(player_input, computer_choice)

        if result == "tie":
            print("It's a tie!\n")
        elif result == "player":
            print("You win this round!\n")
            player_score += 1
        else:
            print("Computer wins this round.\n")
            computer_score += 1


if __name__ == "__main__":
    main()