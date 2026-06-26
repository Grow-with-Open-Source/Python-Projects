import random
import string
from typing import List

def generate_number_only(length: int) -> str:
    """Generates a password consisting only of digits.

    Args:
        length: The length of the password.

    Returns:
        A string of random digits.
    """
    digits = string.digits
    return "".join(random.choice(digits) for _ in range(length))


def generate_letters_only(length: int) -> str:
    """Generates a password consisting only of letters.

    Args:
        length: The length of the password.

    Returns:
        A string of random letters.
    """
    letters = string.ascii_letters
    return "".join(random.choice(letters) for _ in range(length))


def generate_symbols_only(length: int) -> str:
    """Generates a password consisting only of symbols.

    Args:
        length: The length of the password.

    Returns:
        A string of random symbols.
    """
    symbols = "!@#$%^&*()-_=+[]{};:,.<>?/\\|"
    return "".join(random.choice(symbols) for _ in range(length))


def mix_of_all(length: int) -> str:
    """Generates a password consisting of letters, digits, and symbols.

    Args:
        length: The length of the password.

    Returns:
        A string of random mixed characters.
    """
    pool = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.<>?/\\|"
    return "".join(random.choice(pool) for _ in range(length))


def _get_composition(password: str) -> tuple:
    """Counts character types in a password.

    Args:
        password: The password string to analyze.

    Returns:
        A tuple of (upper, lower, digits, symbols) counts.
    """
    upper = lower = digits = symbols = 0
    for char in password:
        if char.isupper():
            upper += 1
        elif char.islower():
            lower += 1
        elif char.isdigit():
            digits += 1
        else:
            symbols += 1
    return upper, lower, digits, symbols


def password_report(password: str) -> str:
    """Generates a security report for a given password.

    Args:
        password: The password string to analyze.

    Returns:
        A human-readable report string.
    """
    recommended_length = 8
    length = len(password)
    upper, lower, digits, symbols = _get_composition(password)

    parts = []

    if length < recommended_length:
        parts.append(
            f"The password has a length of {length} characters, {recommended_length - length} less than the recommended {recommended_length}."
        )
    else:
        parts.append(
            f"The password has a length of {length} characters, which meets or exceeds the recommended {recommended_length}."
        )

    parts.append(
        f"It has {upper} uppercase letter(s), {lower} lowercase letter(s), {digits} number(s), and {symbols} symbol(s)."
    )

    suggestions = []
    if upper == 0:
        suggestions.append("add at least one uppercase letter")
    if lower == 0:
        suggestions.append("add at least one lowercase letter")
    if digits == 0:
        suggestions.append("add at least one number")
    if symbols == 0:
        suggestions.append("add a symbol for extra strength")

    if suggestions:
        parts.append("To improve this password, you could " + ", ".join(suggestions) + ".")
    else:
        parts.append("This password has a good mix of character types.")

    return " ".join(parts)


def main() -> None:
    """Main function for interactive password generation and checking."""
    option = ""
    while option not in ("1", "2"):
        option = input(
            "What would you like to do:\n"
            "1 Generate a secure password\n"
            "2 Check the strength of my password\n> "
        )
        if option not in ("1", "2"):
            print("Please choose 1 or 2.")

    if option == "1":
        _handle_password_generation()
    else:
        existing = input("Enter the password you want to check: ")
        print(password_report(existing))


def _handle_password_generation() -> None:
    """Handles the password generation flow."""
    choice = 0
    while choice not in (1, 2, 3, 4):
        try:
            choice = int(
                input(
                    "Choose password type:\n"
                    "1 Mix of numbers, letters and symbols (Recommended)\n"
                    "2 Numbers only password\n"
                    "3 Letters only password\n"
                    "4 Symbols only password\n> "
                )
            )
        except ValueError:
            print("Invalid input, enter numbers only.")

    length = 0
    while length not in range(4, 21):
        try:
            length = int(input("Enter your desired length (between 4 and 20): "))
        except ValueError:
            print("Invalid input, enter numbers only.")

    passwd_map = {
        1: mix_of_all,
        2: generate_number_only,
        3: generate_letters_only,
        4: generate_symbols_only,
    }

    passwd = passwd_map[choice](length)
    print("Here is your password:", passwd)

    if input("Would you like a report for this password? (y/n): ").lower() == "y":
        print(password_report(passwd))


if __name__ == '__main__':
    main()
