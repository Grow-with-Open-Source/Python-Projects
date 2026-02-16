import pyautogui
import keyboard
import time


def run_auto_clicker(delay: float = 0.01) -> None:
    """
    Runs an auto clicker that can be controlled with keyboard hotkeys.

    Controls:
    - Press 'S' to start clicking
    - Press 'E' to stop clicking
    - Press 'Q' to quit
    """
    clicking = False

    def start_clicking():
        nonlocal clicking
        clicking = True
        print("✅ Auto clicker started")

    def stop_clicking():
        nonlocal clicking
        clicking = False
        print("⏹ Auto clicker stopped")

    keyboard.add_hotkey("s", start_clicking)
    keyboard.add_hotkey("e", stop_clicking)

    print("Press 'S' to start clicking")
    print("Press 'E' to stop clicking")
    print("Press 'Q' to quit")

    try:
        while True:
            if clicking:
                pyautogui.click()
                time.sleep(delay)

            if keyboard.is_pressed("q"):
                print("👋 Exiting program")
                break

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")


if __name__ == "__main__":
    run_auto_clicker()
