import time
import datetime


FOCUS_DURATION = 25 * 60       # 25 minutes
SHORT_BREAK = 5 * 60           # 5 minutes
LONG_BREAK = 20 * 60           # 20 minutes
SESSIONS_BEFORE_LONG_BREAK = 4


def countdown(label, seconds):
    """Runs a countdown timer."""
    while seconds > 0:
        timer = datetime.timedelta(seconds=seconds)
        print(f"{label} - Time left: {timer}", end="\r")
        time.sleep(1)
        seconds -= 1
    print(f"\n{label} completed!\n")


def pomodoro_timer(task, total_seconds):
    """Runs Pomodoro cycles based on total time."""
    sessions_completed = 0

    while total_seconds > 0:
        print(f"\nStarting focus session for: {task}")
        session_time = min(FOCUS_DURATION, total_seconds)
        countdown("Focus Session", session_time)
        total_seconds -= session_time
        sessions_completed += 1

        if total_seconds <= 0:
            break

        if sessions_completed % SESSIONS_BEFORE_LONG_BREAK == 0:
            print("Starting Long Break...")
            countdown("Long Break", LONG_BREAK)
        else:
            print("Starting Short Break...")
            countdown("Short Break", SHORT_BREAK)

    print("Task Completed Successfully 🎉")


def get_user_input():
    """Handles validated user input."""
    try:
        task = input("Enter the task to focus on: ")

        h = int(input("Enter hours: "))
        m = int(input("Enter minutes: "))
        s = int(input("Enter seconds: "))

        if h < 0 or m < 0 or s < 0:
            raise ValueError("Time values cannot be negative.")

        return task, h * 3600 + m * 60 + s

    except ValueError as e:
        print(f"Invalid input: {e}")
        return None, None


if __name__ == "__main__":
    try:
        task, total_seconds = get_user_input()

        if task and total_seconds:
            pomodoro_timer(task, total_seconds)

    except KeyboardInterrupt:
        print("\nTimer stopped manually.")
