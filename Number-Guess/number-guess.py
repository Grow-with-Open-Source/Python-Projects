from random import randrange

def main():
    print("Welcome to Number Guessing Game!")
    level = 1
    total_score = 0

    while True:
        print(f"\n--- Level {level} ---")
        max_number = get_level_max(level)
        randomized_no = randrange(1, max_number + 1)
        attempts_left = 5  # max attempts per level

        while attempts_left > 0:
            user_guess = get_guess(level)
            if user_guess > randomized_no:
                print("Too high! Try again.")
            elif user_guess < randomized_no:
                print("Too low! Try again.")
            else:
                print(f"Correct! You've cleared Level {level}.")
                total_score += attempts_left * 10  # more points for fewer attempts
                break
            attempts_left -= 1
            print(f"Attempts left: {attempts_left}")
        else:
            print(f"Game Over! The number was {randomized_no}.")
            break

        level += 1
        print(f"Total Score: {total_score}")
        cont = input("Do you want to continue to the next level? (y/n): ").lower()
        if cont != 'y':
            print(f"Thanks for playing! Final Score: {total_score}")
            break

def is_positive_integer(n):
    try:
        num = int(n)
        return num > 0
    except ValueError:
        return False

def get_guess(level):
    while True:
        guess_input = input(f"Level {level} Guess: ")
        if is_positive_integer(guess_input):
            return int(guess_input)
        else:
            print("Enter a valid positive integer!")

def get_level_max(level):
    """Increase range as levels go up"""
    return 10 + (level - 1) * 5

if __name__ == "__main__":
    main()
