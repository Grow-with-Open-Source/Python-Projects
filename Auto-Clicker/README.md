# Auto Clicker

A Python automation tool that allows you to automatically click the mouse at rapid intervals. This is useful for repetitive clicking tasks and can be controlled via keyboard hotkeys.

## Features

- Start and stop automatic clicking with keyboard hotkeys
- Adjustable click interval (currently set to 1ms between clicks)
- Simple keyboard controls for easy on/off toggling
- Minimal resource usage

## Requirements

- Python 3.x
- pyautogui library
- keyboard library

## Installation

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## How to Use

1. Run the script by executing the `auto_clicker.py` file:

```bash
python auto_clicker.py
```

2. The program will start and display instructions:
   - Press `'S'` to **start** the auto clicker
   - Press `'E'` to **stop** the auto clicker
   - Press `'Q'` to **quit** the program

3. Once started (by pressing 'S'), the auto clicker will automatically perform mouse clicks at the current cursor position at fixed intervals (Can be edited in the code).

4. Press 'E' to stop the clicking, and press 'Q' to exit the program entirely.

## Caution

⚠️ **WARNING**: Use this tool responsibly. Automated clicking can:
- Interfere with other applications
- Cause unintended actions if not carefully controlled
- May violate terms of service for certain applications or games

Always ensure you have full control over what the auto clicker is doing before starting it.

## How It Works

The script uses the following libraries:

- **pyautogui**: For performing automated mouse clicks
- **keyboard**: For detecting keyboard hotkey presses to control the clicker

The program runs in an infinite loop, continuously checking if the 'q' key is pressed (to exit) and performing clicks when the `clicking` flag is set to `True`.
