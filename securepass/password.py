import random
import string


def main():
    while True:
        option = input(
            "What would you like to do:\n"
            "1 Generate a secure password\n"
            "2 Check strength of my password\n> "
        )
        if option not in ("1", "2"):
            print("Please choose 1 or 2.")
            continue
        break

    if option == "1":
        while True:
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
                length = int(input("Enter your desired length (between 4 and 20): "))
            except ValueError:
                print("Invalid input, enter numbers only.")
                continue

            if choice not in (1, 2, 3, 4) or length not in range(4, 21):
                print("Invalid input, try again.")
                continue
            break

        if choice == 1:
            passwd = mix_of_all(length)
        elif choice == 2:
            passwd = generate_number_only(length)
        elif choice == 3:
            passwd = generate_letters_only(length)
        else:
            passwd = generate_symbols_only(length)

        print("Here is your password:", passwd)

        if input("Would you like a report for this password? (y/n): ").lower() == "y":
            print(password_report(passwd))

    else:  # option == "2"
        existing = input("Enter the password you want to check: ")
        print(password_report(existing))


def generate_number_only(length):
    digits = string.digits
    return "".join(random.choice(digits) for _ in range(length))


def generate_letters_only(length):
    letters = string.ascii_letters
    return "".join(random.choice(letters) for _ in range(length))


def generate_symbols_only(length):
    symbols = "!@#$%^&*()-_=+[]{};:,.<>?/\\|"
    return "".join(random.choice(symbols) for _ in range(length))


def mix_of_all(length):
    pool = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.<>?/\\|"
    return "".join(random.choice(pool) for _ in range(length))


def password_report(password: str) -> str:
    recommended_length = 8

    length = len(password)
    upper = sum(1 for ch in password if ch.isupper())
    lower = sum(1 for ch in password if ch.islower())
    digits = sum(1 for ch in password if ch.isdigit())
    symbols = sum(1 for ch in password if not ch.isalnum())

    parts = []

    # Length report
    diff = recommended_length - length
    if diff > 0:
        parts.append(
            f"The password has a length of {length} characters, {diff} less than the recommended {recommended_length}."
        )
    else:
        parts.append(
            f"The password has a length of {length} characters, which meets or exceeds the recommended {recommended_length}."
        )

    # Composition report
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
        parts.append(
            "To improve this password, you could " + ", ".join(suggestions) + "."
        )
    else:
        parts.append("This password has a good mix of character types.")

    return " ".join(parts)


if __name__ == '__main__':
    main()
