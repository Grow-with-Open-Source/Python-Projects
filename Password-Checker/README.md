# Password-Checker

Password-Checker is a simple script that checks the strength of a given password and provides suggestions to improve its security. It can also suggest a stronger password based on the given input.

You can provide input either as a command-line argument or interactively through the terminal *(interactive mode is recommended)*. This script performs only basic checks and is intended as a minimal example.

> [!IMPORTANT]
> This script serves as a foundational example and may not be fully suitable for real-world use cases. Its purpose is to provide a starting point for learning and further improvements.

---

## Requirements

- Python **3.6 or above**
- No external dependencies required

---

## Usage

### For Unix-based systems

```bash
# Run the script directly
curl -s https://raw.githubusercontent.com/Grow-with-Open-Source/Python-Projects/main/Password-Checker/check-password.py | python

# OR
wget -qO- https://raw.githubusercontent.com/Grow-with-Open-Source/Python-Projects/main/Password-Checker/check-password.py | python

# Alternatively, download the script and run locally:

# Download the script
wget https://raw.githubusercontent.com/Grow-with-Open-Source/Python-Projects/main/Password-Checker/check-password.py

# --- OR ---
# curl -o check-password.py https://raw.githubusercontent.com/Grow-with-Open-Source/Python-Projects/main/Password-Checker/check-password.py

# Give execute permission
chmod +x check-password.py

# Run the script
./check-password.py

### For Windows

# On Windows 10 or later, PowerShell usually includes curl

# Download and run the script temporarily
Invoke-WebRequest https://raw.githubusercontent.com/Grow-with-Open-Source/Python-Projects/main/Password-Checker/check-password.py -OutFile "$env:TEMP\check_password.py"
python "$env:TEMP\check_password.py"

# Alternatively, download the script to a folder and run using Python interpreter

## Contributing

# Before contributing:
# 1. Make sure you have run and understood the script.
# 2. Review the repository’s Contributing Guidelines:
#    https://github.com/Grow-with-Open-Source/Python-Projects/blob/main/CONTRIBUTING.md

# Notes:
# - Since this mini-project is intended as a sample groundwork for enhancements,
#   please record your changes and contributions in the Change Log section.

## Change Log

- PR #37: Created the basic script with minimum features.

## License

This project is released under the Apache License 2.0:
https://github.com/Grow-with-Open-Source/Python-Projects/blob/main/LICENSE
