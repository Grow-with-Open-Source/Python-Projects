## What it does

A terminal-based typing speed test built with Python's `curses` library.
A random sentence is loaded from a text file and displayed on screen.
As the user types, each character turns green for correct and red for
incorrect in real time. Words per minute is calculated and displayed
live throughout the test. The user can play multiple rounds or exit
with ESC at any time.

## Setting Up This Project

### What is `requirements.txt`?

A `requirements.txt` file is a list of external packages your code needs to run, written in a plain text file. Instead of installing each package one by one, anyone can install everything in one command.

### Step 1 — Clone the repository

```bash
git clone https://github.com/Grow-with-Open-Source/Python-Projects.git
cd Python-Projects/typing-speed-test
```

### Step 2 — Create a virtual environment (recommended)

A virtual environment keeps this project's packages separate from everything else on your computer.

```bash
# Create it
python -m venv venv

# Activate it — Windows
venv\Scripts\activate

# Activate it — Mac/Linux
source venv/bin/activate
```

### Step 3 — Install the requirements

```bash
pip install -r requirements.txt
```

This reads `requirements.txt` and installs everything listed inside it automatically.

### Step 4 — Run the program

```bash
python typing_test.py
```

### A note on this project

The `curses` library comes built into Python automatically on Mac and Linux. On Windows it does not, so `requirements.txt` only installs `windows-curses` if you are on Windows — that is what the `; platform_system == "Windows"` condition means. Pip handles this automatically based on your operating system, so you do not need to do anything different.
