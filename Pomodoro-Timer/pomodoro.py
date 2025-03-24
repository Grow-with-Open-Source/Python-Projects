import time
import datetime

# Create a function that acts as a countdown
def pomodoro_timer(task, total_seconds):
    # Counter to keep track of the breaks
    break_count = 0

    while total_seconds > 0:
        # Timer represents time left on the countdown
        timer = datetime.timedelta(seconds=total_seconds)
        print(f"Focusing on {task}... Session time left: {timer}", end="\r")

        # Delay the program one second
        time.sleep(1)
        # Reduces total time by one second
        total_seconds -= 1

       # Check if it's time for a break (only for the first 4 breaks)
        if total_seconds > 0 and break_count < 4 and total_seconds % 1500 == 0:
            print("\nNow on a short break!")
            time.sleep(300)  # 5-minute short break
            break_count += 1

        # Check if it's time for a long break (after 4 sessions)
        elif total_seconds > 0 and break_count == 4 and total_seconds % 1500 == 0:
            print("\nNow on a long break!")
            time.sleep(1200)  # Long break for 20 minutes
            break_count = 0  # Reset the break count for the next cycle

    print("\nTask Completed")

# Get user input (In HH:MM:SS format)
task = input("Enter the task to focus on: ")
time_input = input("Enter time in HH:MM:SS format (e.g., 00:25:00 for 25 min): ")

# Convert input time to seconds
h, m, s = map(int, time_input.split(":"))
total_seconds = h * 3600 + m * 60 + s
pomodoro_timer(task, total_seconds)
