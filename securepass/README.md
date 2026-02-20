# Secure Password Manager

A Python utility for generating secure passwords and checking the strength of existing passwords.

## Features

- **Password Generator**: Create secure passwords with multiple options
  - Mix of numbers, letters, and symbols (Recommended)
  - Numbers only
  - Letters only
  - Symbols only
  - Customizable length (4-20 characters)

- **Password Strength Checker**: Analyze password quality and get recommendations
  - Check password length
  - Analyze character composition (uppercase, lowercase, numbers, symbols)
  - Receive suggestions for improvement
  - Detailed password report

## Installation

No external dependencies are required. This script uses only Python standard library modules.

```bash
# Clone or download the repository
# Navigate to the securepass directory
cd securepass

# Run the script
python password.py
```

## Usage

Run the script and follow the interactive prompts:

```bash
python password.py
```

### Main Menu

You'll be presented with two options:
1. **Generate a secure password** - Create a new password with custom specifications
2. **Check strength of my password** - Analyze an existing password

### Generate Password Workflow

1. Select the password type (1-4)
2. Enter desired length (4-20 characters)
3. View your generated password
4. Optionally get a detailed password report

### Check Password Strength Workflow

1. Enter the password you want to check
2. Receive a detailed report with recommendations

## Example Output

```
What would you like to do:
1 Generate a secure password
2 Check strength of my password
> 1

Choose password type:
1 Mix of numbers, letters and symbols (Recommended)
2 Numbers only password
3 Letters only password
4 Symbols only password
> 1

Enter your desired length (between 4 and 20): 12
Here is your password: aB3!xK9$mQ2@

Would you like a report for this password? (y/n): y
The password has a length of 12 characters, which meets or exceeds the recommended 8. 
It has 2 uppercase letter(s), 2 lowercase letter(s), 3 number(s), and 3 symbol(s). 
This password has a good mix of character types.
```

## Password Strength Criteria

The password strength checker evaluates:

- **Length**: Recommends a minimum of 8 characters
- **Character Diversity**: Checks for presence of:
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Symbols

## Functions

- `generate_number_only(length)` - Generates password with digits only
- `generate_letters_only(length)` - Generates password with letters only
- `generate_symbols_only(length)` - Generates password with symbols only
- `mix_of_all(length)` - Generates password with mix of all character types
- `password_report(password)` - Analyzes password strength and returns report

## Requirements

- Python 3.x
- No external packages required

## Best Practices

- Use "Mix of numbers, letters and symbols" for the strongest passwords
- Maintain a minimum length of 12 characters for sensitive accounts
- Store generated passwords securely (consider using a password manager)
- Regularly update passwords for important accounts
- Never share passwords or store them in plain text

## License

This project is part of the Python-Projects repository by Grow-with-Open-Source.
