import pyautogui
import keyboard
import time

clicking = False


def start_clicking():
    global clicking
    clicking = True
    print("Auto clicker started")


def stop_clicking():
    global clicking
    clicking = False
    print("Auto clicker stopped")


keyboard.add_hotkey("s", start_clicking)
keyboard.add_hotkey("e", stop_clicking)

print("Press 'S' to start clicking")
print("Press 'E' to stop clicking")
print("Press 'Q' to quit")

while True:
    if clicking:
        pyautogui.click()
        time.sleep(0.001)

    if keyboard.is_pressed("q"):
        print("Exiting program")
        break
