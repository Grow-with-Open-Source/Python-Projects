import time
import datetime

# Create a function that acts as a countdown
def pomodoro_timer(task, h, m, s):
    # Calculate the total number of seconds
    total_seconds = h * 3600 + m * 60 + s

    # Counter to keep track of the breaks
    break_count = 0

    while total_seconds > 0:
        # Timer represents time left on the countdown
        timer = datetime.timedelta(seconds=total_seconds)
        # Prints the time left on the timer
        print(f"Focusing on {task}... Session time left: {timer}", end="\r")

        # Delays the program one second
        time.sleep(1)

        # Reduces total time by one second
        total_seconds -= 1

        # Check if it's time for a break (only for the first 4 breaks)
        if total_seconds > 0 and break_count < 4 and total_seconds % 1500 == 0:
            print("\nNow on a short break!")
            time.sleep(300)  # Short break for 5 minutes
            break_count += 1

        # Check if it's time for a long break (after 4 sessions)
        elif total_seconds > 0 and break_count == 4 and total_seconds % 1500 == 0:
            print("\nNow on a long break!")
            time.sleep(1200)  # Long break for 20 minutes
            break_count = 0  # Reset the break count for the next cycle

    print("\nTask Completed")

# Inputs for hours, minutes, and seconds on the timer
task = input("Enter the task to focus on: ")
h = int(input("Enter the time in hours: "))
m = int(input("Enter the time in minutes: "))
s = int(input("Enter the time in seconds: "))
pomodoro_timer(task, h, m, s)
