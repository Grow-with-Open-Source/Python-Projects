import random

def check_guess(guess, answer):
    """Check user's guess and return True if correct."""
    attempt = 0
    while attempt < 3:
        if guess.lower() == answer.lower():
            print("✅ Correct Answer!\n")
            return True
        else:
            attempt += 1
            if attempt < 3:
                guess = input("❌ Wrong! Try again: ")
    print(f"The correct answer is: {answer}\n")
    return False


def main():
    print("🐾 Welcome to the Animal Guessing Game! 🐾")
    print("You have 3 attempts for each question.\n")

    questions = {
        "Which bear lives at the North Pole?": "polar bear",
        "Which is the fastest land animal?": "cheetah",
        "Which is the largest animal?": "blue whale",
        "Which animal is known as the king of the jungle?": "lion",
        "Which animal can sleep standing up?": "horse"
    }

    score = 0
    # Randomize question order
    for question, answer in random.sample(list(questions.items()), 3):
        guess = input(question + " ")
        if check_guess(guess, answer):
            score += 1

    print(f"🎯 Your final score is: {score}/{len(questions)}")

    # Option to play again
    replay = input("\nDo you want to play again? (yes/no): ")
    if replay.lower().startswith('y'):
        print("\nRestarting game...\n")
        main()
    else:
        print("Thanks for playing! 🦋")


if __name__ == "__main__":
    main()
