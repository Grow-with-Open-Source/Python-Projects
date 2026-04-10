# Spell-Sense: Advanced Spell Checker

Spell-Sense is a professional, modular Python application that provides real-time spelling suggestions. Built with `Tkinter` and `TextBlob`, it improves upon basic implementations by adding robust error handling and a clean, user-friendly interface.

## Features
- Smart Validation: Detects empty inputs and prevents unnecessary processing.
- Color-Coded Feedback: Uses visual cues (Green for success, Blue for suggestions, Red for errors).
- Modular Design: Separation of concerns between UI logic and processing logic.
- Keyboard Friendly: Press `Enter` to check spelling instantly without clicking.
- Auto-Focus: The cursor starts in the input box for immediate typing.

## Project Structure
/Spell-Sense/
├── main.py            # Entry point and UI (Tkinter)
├── logic.py           # Core NLP logic (TextBlob)
├── requirements.txt   # Dependency list
└── README.md          # Documentation

🚀 Installation & Setup
Prerequisites
Python 3.6 or higher

Setup
Navigate to your project directory:

Bash
cd Spell-Sense
Install the required dependencies:

Bash
pip install -r requirements.txt
🛠️ Usage
Run the script from your terminal:

Bash
python main.py
Type a word into the input box.

Press Enter or click Check.

View the suggestion or success message below.

Click Reset to clear the fields.

📝 Credits
This project was developed as an enhanced alternative to basic scripts in this repository. It focuses on modularity, error handling, and improved User Experience (UX).

License
This project is open-source and intended for educational use.