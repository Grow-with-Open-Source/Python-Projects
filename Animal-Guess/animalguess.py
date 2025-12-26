
# Improved version with modular structure, input validation, and typo fixes

def check_guess(guess, answer):
    """
    Checks the user's guess against the correct answer.
    Allows up to 3 attempts.
    Returns 1 if correct, 0 otherwise.
    """
    attempt = 0
    while attempt < 3:
        if guess.lower().strip() == answer.lower():
            print("✅ Correct Answer!")
            return 1  # increment score
        else:
            attempt += 1
            if attempt < 3:
                guess = input("❌ Wrong answer. Try again: ").strip()
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
        guess = input(question + " ").strip()
        while not guess:
            guess = input("Please enter a valid guess: ").strip()
        score += check_guess(guess, answer)

    print(f"\n🏆 Your Total Score is: {score} out of {len(questions)}")

if __name__ == "__main__":
    main()
