#!/usr/bin/env python
import re
import sys
import random
from getpass import getpass

# ANSI escape codes for colors
COLOR = {
    "RED": '\033[91m',
    "YELLOW": '\033[93m',
    "GREEN": '\033[92m',
    "BLUE": '\033[94m',
    "RESET": '\033[0m'
}

KEYBOARD_PATTERNS = ['qwerty', 'asdfgh', 'zxcvbn']
COMMON_SUBSTITUTIONS = {
    '@': 'a', '4': 'a', '3': 'e', '0': 'o',
    '1': 'i', '$': 's', '7': 't'
}

COMMON_WORDS = {
    'adjectives': ['Happy', 'Clever', 'Swift', 'Brave', 'Bright'],
    'nouns': ['Tiger', 'River', 'Mountain', 'Storm', 'Star'],
    'numbers': ['365', '42', '777', '314', '999'],
    'separators': ['_', '.', '#', '*', '@']
}

PATTERNS = {
    'uppercase': re.compile(r'[A-Z]'),
    'lowercase': re.compile(r'[a-z]'),
    'numbers': re.compile(r'\d'),
    'special': re.compile(r'[!@#$%^&*(),.?":{}|<>]')
}


def format_to_header(
        msg: str,
        *,
        rep: float = 1,
        new_line_at_end: bool = False,
        is_main_header: bool = False):
    if not isinstance(msg, str):
        raise TypeError("msg must be a string")

    res_str = "\n"
    no_of_hypens = int(len(msg)*rep)

    if is_main_header:
        no_of_hypens += 4
        msg = f"| {msg.upper()} |"

    header_str = [
        '-'*no_of_hypens,
        msg,
        '-'*no_of_hypens,
    ]

    res_str += "\n".join(header_str)
    if new_line_at_end:
        res_str += "\n"
    return res_str


def check_password_strength(password):
    score = 0
    suggestions = []

    # Check length
    if len(password) < 12:
        suggestions.append("Password should be at least 12 characters long.")
    elif len(password) >= 16:
        score += 2
    else:
        score += 1

    # Check for uppercase
    if not PATTERNS['uppercase'].search(password):
        suggestions.append("Add uppercase letters.")
    else:
        score += 1

    # Check for lowercase
    if not PATTERNS['lowercase'].search(password):
        suggestions.append("Add lowercase letters.")
    else:
        score += 1

    # Check for numbers
    if not PATTERNS['numbers'].search(password):
        suggestions.append("Add numbers.")
    else:
        score += 1

    # Check for special characters
    if not PATTERNS['special'].search(password):
        suggestions.append("Add special characters.")
    else:
        score += 1

    # Check for repeated patterns (like 'testtest')
    half_length = len(password) // 2
    for i in range(2, half_length + 1):
        if password[:i] * (len(password) // i) == password[:len(password) // i * i]:
            suggestions.append("Avoid repeating patterns in your password.")
            score -= 1
            break

    # Check for keyboard patterns
    lower_pass = password.lower()
    for pattern in KEYBOARD_PATTERNS:
        if pattern in lower_pass:
            suggestions.append("Avoid common keyboard patterns")
            score -= 1
            break

    # Check for simple character substitutions
    substituted = password.lower()
    for k, v in COMMON_SUBSTITUTIONS.items():
        substituted = substituted.replace(k, v)
    if substituted.isalpha() and len(substituted) > 3:
        suggestions.append(
            "Using symbol substitutions (like '@' for 'a') isn't very secure.")
        score -= 1

    # Ensure score doesn't go below 0
    score = max(0, score)

    return score, suggestions


def categorize_password(score):
    if score < 2:
        return "WEAK", COLOR["RED"]
    if score < 4:
        return "GOOD", COLOR["YELLOW"]
    return "STRONG", COLOR["GREEN"]


def create_memorable_suggestion(base_word):
    adj = random.choice(COMMON_WORDS['adjectives'])
    noun = random.choice(COMMON_WORDS['nouns'])
    num = random.choice(COMMON_WORDS['numbers'])
    sep = random.choice(COMMON_WORDS['separators'])

    # Use the base word if it's good enough (not too short and has letters)
    if len(base_word) >= 4 and any(c.isalpha() for c in base_word):
        base = base_word.capitalize()
    else:
        base = noun

    patterns = [
        f"{adj}{sep}{base}{num}",
        f"{base}{sep}{noun}{num}",
        f"{num}{sep}{adj}{base}"
    ]

    return random.choice(patterns)


def suggest_better_password(password):
    # If password is very weak, create a completely new memorable one
    score, _ = check_password_strength(password)
    if score < 2:
        return create_memorable_suggestion(password)

    suggestion = password

    # Smart character substitutions (maintain readability)
    smart_subs = {
        'a': '@', 'e': '3', 'i': '!', 'o': '0', 's': '$',
        'ate': '8', 'to': '2', 'for': '4'
    }

    # Apply substitutions intelligently
    for word, replacement in smart_subs.items():
        if word in suggestion.lower() and random.random() < 0.5:  # 50% chance
            suggestion = suggestion.replace(word, replacement)

    # Ensure at least one capital letter in a natural position
    if not any(c.isupper() for c in suggestion):
        words = suggestion.split()
        if words:
            words[0] = words[0].capitalize()
            suggestion = ''.join(words)

    # Add complexity if needed while keeping it memorable
    if len(suggestion) < 12:
        suggestion += random.choice(COMMON_WORDS['numbers'])

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', suggestion):
        suggestion += random.choice(COMMON_WORDS['separators'])

    return suggestion


def input_handler():
    if len(sys.argv) > 1:
        password = sys.argv[1]
        print(
            f"{COLOR['RED']}It is recommended to avoid entering passwords directly on the command line,{COLOR['RESET']}")
        print(
            f"{COLOR['RED']}as they may be visible to others and recorded in the shell history.{COLOR['RESET']}")
        return password
    print(
        format_to_header(
            "Password Strength Checker",
            new_line_at_end=True,
            is_main_header=True
        )
    )
    print("For enhanced security, your input will be hidden.")
    print("Hence, you may not see the characters as you type.")
    try:
        password = getpass("\nEnter password to check: ")
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    return password


def output_handler(password, category, color, suggestions):
    print(f"\nPassword Strength: {color}{category}{COLOR['RESET']}")

    if suggestions:
        print(format_to_header("Suggestions to improve:"))
        for suggestion in suggestions:
            print(f"{COLOR['BLUE']}- {suggestion}{COLOR['RESET']}")

    # Add this block to show suggested password
    if category != "STRONG":
        better_password = suggest_better_password(password)
        print(
            f"\nSuggested stronger password: {COLOR['GREEN']}{better_password}{COLOR['RESET']}")

    points_to_remember = [
        "Never use your personal information while creating a password.",
        "Consider using a passphrase made up of multiple words for better security.",
        "Avoid using common phrases or easily guessable patterns.",
        "Avoid using the same password for multiple accounts.",
        "Regularly update your passwords to enhance security.",
        "Use a reputable password manager to generate and store complex passwords securely."
    ]
    print(format_to_header('Points to Remember:'))
    for points in points_to_remember:
        print(f"{COLOR['BLUE']}- {points}{COLOR['RESET']}")


def main():
    password = input_handler()
    score, suggestions = check_password_strength(password)
    category, color = categorize_password(score)
    output_handler(password, category, color, suggestions)


if __name__ == "__main__":
    main()
