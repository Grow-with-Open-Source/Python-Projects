import time
import datetime
def pomodoro_timer(task, h, m, s):
total_seconds = h * 3600 + m * 60 + s
break_count = 0
while total_seconds > 0:
timer = datetime.timedelta(seconds=total_seconds)
print(f"Focusing on {task}... Session time left: {timer}", end="\r")
time.sleep(1)
total_seconds -= 1
if total_seconds > 0 and break_count < 4 and total_seconds % 1500 == 0:
print("\nNow on a short break!")
time.sleep(300)
break_count += 1
elif total_seconds > 0 and break_count == 4 and total_seconds % 1500 == 0:
print("\nNow on a long break!")
time.sleep(1200)
break_count = 0
print("\nTask Completed")
task = input("Enter the task to focus on: ")
h = int(input("Enter the time in hours: "))
m = int(input("Enter the time in minutes: "))
s = int(input("Enter the time in seconds: "))
pomodoro_timer(task, h, m, s)
