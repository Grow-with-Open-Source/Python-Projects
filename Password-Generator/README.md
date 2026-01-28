# Secure Password Generator

A secure and customizable password generator built with Python that creates cryptographically strong passwords using the `secrets` module.

## Features

- Generates cryptographically secure passwords
- Customizable password length (6-128 characters)
- Option to include/exclude digits and symbols
- Generates multiple passwords at once
- Save passwords to a text file
- Input validation and error handling

## Installation

### Prerequisites
- Python 3.6 or higher

### Setup
1. Clone or download the `password.py` file to your local machine
2. No additional dependencies required - uses only Python's standard library

### In Terminal
```bash
git clone https://github.com/Grow-with-Open-Source/Python-Projects.git
cd Python-Projects
cd Password-Generator 
python password.py
```

## Usage

Run the script from your terminal or command prompt:

```bash
python password.py
```

### In your own script
```python
from password import generate_password

# Generate a single password
password = generate_password(length=12, digits=True, symbols=True)
print(password)

# Generate without symbols
simple_password = generate_password(length=10, digits=True, symbols=False)
print(simple_password)
```

## Running Examples
### Example 1: Basic Password Generation

```python
> python password.py
Enter the length of the password: 12
Enter the number of passwords to generate: 3
Include digits? (y/n): y
Include symbols? (y/n): y

Generating Secure Passwords...

Password #1: aB3@kL9#mN2!
Password #2: pQ8$rS1^tU4*
Password #3: xY7&zW5!vZ9@

Do you want to save the passwords to a file? (y/n): y
Enter the name of the file (without .txt): my_passwords

Saving passwords to file...
Passwords saved successfully!
```

### Example 2: Simple Alphanumeric Passwords
```python
> python password.py
Enter the length of the password: 8
Enter the number of passwords to generate: 2
Include digits? (y/n): y
Include symbols? (y/n): n

Generating Secure Passwords...

Password #1: aB3cD9eF
Password #2: gH4iJ7kL
```

### Example 3: Short Password (Auto-corrected)
```python
> python password.py
Enter the length of the password: 4
Enter the number of passwords to generate: 1
Include digits? (y/n): y
Include symbols? (y/n): y

Password is too short - Generating Passwords of length 6

Generating Secure Passwords...

Password #1: a@3b#9
```

## Interactive Options
When you run the script, you'll be prompted for the following:

1. Password Length: Enter an integer between 6 and 128
- If you enter less than 6, it will automatically set to 6
- Maximum length is 128 characters

2. Number of Passwords: How many passwords to generate (positive integer)

3. Include Digits?: (y/n) - Whether to include numbers (0-9)

4. Include Symbols?: (y/n) - Whether to include special characters (!@#$%^&*(), etc.)

5. Save to File?: (y/n) - Option to save generated passwords to a text file
- If yes, you can specify a filename (default: "passwords.txt")

## Password Security Features
1. **Cryptographically Secure**: Uses ``secrets`` module (not ``random``) for true randomness

2. **Character Variety**: Ensures at least one character from each selected character set

3. **Shuffling**: Passwords are shuffled after generation to avoid predictable patterns

4. **Length Enforcement**: Minimum 6 characters for basic security

5. **Input Validation**: Validates all user inputs to prevent errors

## File Structure
```text
password.py
├── generate_password(length, digits, symbols)  # Core generator function
├── save(passwords)                            # File saving function
└── main()                                     # Interactive CLI interface
```

## Error Handling
The script includes comprehensive error handling for:

- Invalid integer inputs
- File system errors when saving
- Unexpected exceptions
- Length constraints and requirements

## Limitations
- Maximum password length is 128 characters
- Minimum password length is 6 characters (enforced)
- Uses standard Python string punctuation for symbols
- Text file saving is optional and basic

## Security Notes
- ✅ Uses secrets module for cryptographically secure random generation
- ✅ No external dependencies or network calls
- ✅ Passwords are generated locally on your machine
- ❗ Saved passwords are stored in plain text - handle with care!
- ❗ Always use strong, unique passwords for different services

## License
This project is open-source and intended for educational and practical use.
Refer to the repository license for usage terms.