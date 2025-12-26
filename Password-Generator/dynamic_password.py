"""_summary_
    implementing password generation program that allows symbols and capital letters if the user wants to include them

    Returns:
        password
"""



import random


#constants
SMALL_LETTERS="abcdefghijklmnopqrstuvwxyz"
CAPITAL_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SYMBOLS="~!@#$%^&*()_-+={[}]|:;<>?"
MIN_LENGTH=12
MAX_LENGTH=24


#function to generate the password
def dynamic_password(passlength,capitals=False,symbols=False):
    characters=SMALL_LETTERS
    if capitals:
        characters+=CAPITAL_LETTERS
    if symbols:
        characters+=SYMBOLS
    password=""
    for i in range(0,passlength):
        randomletter=random.choice(characters)
        password+=(randomletter)

    return password

#Function to take user inputs and validate them
def inputs_validation():
     while True:

        pass_length=input(f"Enter password length ({MIN_LENGTH}-{MAX_LENGTH}): ")
        input_capitals=input("Do we include capitals (y/n): ").strip().lower()
        input_symbols=input("Do we include symbols (y/n): ").strip().lower()

        # 1. Validate both inputs at once
        if input_capitals not in ['y', 'n'] or input_symbols not in ['y', 'n']:
            print("Please type 'y' or 'n' for the options.")
            continue  # Restarts the loop to ask again
          
        #2. convert to booleans
        capitals=(input_capitals=='y')
        symbols=(input_symbols=='y')

        if pass_length.isdigit():
            #validate password length
            length=int(pass_length)
            if 12<=length<=24:
                return length,capitals,symbols
            else:
                print("Please enter password length within the range!!")
                continue
        print("Password length should be a Number")
            
            



def main():
    length,capitals,symbols=inputs_validation()
    password=dynamic_password(length,capitals,symbols)
    print(f"Your Generated Password is : {password}")


if __name__ == "__main__":
    main()