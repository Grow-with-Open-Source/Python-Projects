"""
Password generation program that allows symbols and capital letters 
based on user preferences.

Returns:
    str: Generated password
"""

import random

# Constants
SMALL_LETTERS = "abcdefghijklmnopqrstuvwxyz"
CAPITAL_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SYMBOLS = "~!@#$%^&*()_-+={[}]|:;<>?"
MIN_LENGTH = 12
MAX_LENGTH = 24


def dynamic_password(passlength, capitals=False, symbols=False):
    """
    Generate a random password based on specified criteria.
    
    Args:
        passlength (int): Length of the password
        capitals (bool): Whether to include capital letters
        symbols (bool): Whether to include symbols
        
    Returns:
        str: Generated password
    """
    # Start with small letters as the base character set
    characters = SMALL_LETTERS
    
    # Add capital letters if requested
    if capitals:
        characters += CAPITAL_LETTERS
        
    # Add symbols if requested
    if symbols:
        characters += SYMBOLS
    
    # Generate password by randomly selecting characters
    password = ""
    for i in range(0, passlength):
        random_letter = random.choice(characters)
        password += random_letter

    return password


def inputs_validation():
    """
    Get and validate user inputs for password generation.
    
    Returns:
        tuple: (length, capitals, symbols) - validated user preferences
    """
    while True:
        # Get user inputs
        pass_length = input(f"Enter password length ({MIN_LENGTH}-{MAX_LENGTH}): ")
        input_capitals = input("Do we include capitals (y/n): ").strip().lower()
        input_symbols = input("Do we include symbols (y/n): ").strip().lower()

        # 1. Validate both yes/no inputs at once
        if input_capitals not in ['y', 'n'] or input_symbols not in ['y', 'n']:
            print("Please type 'y' or 'n' for the options.")
            continue  # Restart the loop to ask again
        
        # 2. Convert inputs to booleans
        capitals = (input_capitals == 'y')
        symbols = (input_symbols == 'y')

        # 3. Validate password length
        if pass_length.isdigit():
            length = int(pass_length)
            
            # Check if length is within valid range
            if MIN_LENGTH <= length <= MAX_LENGTH:
                return length, capitals, symbols
            else:
                print("Please enter password length within the range!!")
                continue
                
        print("Password length should be a number")


def main():
    """Main function to orchestrate the password generation process."""
    # Get validated user inputs
    length, capitals, symbols = inputs_validation()
    
    # Generate password
    password = dynamic_password(length, capitals, symbols)
    
    # Display the generated password
    print(f"Your Generated Password is: {password}")


if __name__ == "__main__":
    main()