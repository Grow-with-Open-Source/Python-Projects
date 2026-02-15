def normalize_input(text):
    """
    Normalize user input for comparison.
    Strips whitespace and converts to lowercase.
    """
    return text.strip().lower()


def check_guess(guess, answer):
    """
    Checks the user's guess against the correct answer.
    Allows up to 3 attempts.
    Returns 1 if correct, 0 otherwise.
    """
    attempt = 0

    while attempt < 3:
        if normalize_input(guess) == normalize_input(answer):
            print("✅ Correct Answer!")
            return 1
        else:
            attempt += 1
            if attempt < 3:
                guess = input("❌ Wrong answer. Try again: ")

    print("The correct answer is:", answer)
    return 0


def main():
    """
    Main game function. Loops through all questions and calculates the total score.
    """
    questions = [
        ("Which bear lives at the North Pole?", "polar bear"),
        ("Which is the fastest land animal?", "cheetah"),
        ("Which is the largest animal?", "blue whale")
    ]

    print("🦁 Welcome to 'Guess the Animal' Game! 🐘")
    score = 0

    for question, answer in questions:
        guess = input(question + " ")

        while not guess.strip():
            guess = input("Please enter a valid guess: ")

        score += check_guess(guess, answer)

    print(f"\n🏆 Your Total Score is: {score} out of {len(questions)}")


if __name__ == "__main__":
    main()
