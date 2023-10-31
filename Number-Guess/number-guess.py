from random import randrange
def main():
    randomized_no = randomize_no()
    while True:
        user_guessed_input = guess()
        if int(user_guessed_input) > randomized_no:
            print("Too large!")
            continue
        elif int(user_guessed_input) < randomized_no:
            print("Too small!")
            continue
        else:
            print("Just right!")
            break
def is_positive_integer(n):
    """This function takes an input and check if the user input is an integer"""
    while True:
        try:
            num = int(n)
            if int(num) < 1:
                return False
        except ValueError:
            return False
        else:
            return True
def get_user_input():
    """Prompt the user for an input and check if it's a positive integer"""
    while True:
        user_input = input("Level 1: ")
        if (is_positive_integer(user_input)):
            return int(user_input)
def guess():
    "Prompt the user for an input guess, and check if it's an integer"
    while True:
        user_guess = input("Guess: ")
        if is_positive_integer(user_guess):
            return user_guess
def randomize_no():
    """Randomize number"""
    user_inputted_number = get_user_input()
    if int(user_inputted_number) > 1:
        random_number = randrange(1,  user_inputted_number)
        return random_number
    else:
        return int(user_inputted_number)
if __name__ == "__main__":
    main()
