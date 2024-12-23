import tkinter as tk
import time
from tkinter.font import Font



def clocks():
    '''
    This function displays the current time.
    '''
    currentTime = time.gmtime()
    currentTime = f'{currentTime.tm_hour}:{currentTime.tm_min}:{currentTime.tm_sec}'
    clock.config(text=currentTime)
    clock.after(200, clocks)
    '''
This is simply printing out to verify whether it is functioning correctly or not.
    '''
    print("Working Properly")


'''
Here I created a instance of TK  class
'''
window = tk.Tk()
# creating a title
window.title("Digital Clock")
# creating background color
window.config(bg="black")

font1 = Font(family="Arial", size=90, weight="normal")
# creating a header using Label Widget
header = tk.Label(window, text="Time Clock", font=font1, bg="gray", fg="white")
# using grid() to place the header somewhere comfortable in the gui
header.grid(row=1, column=2)
'''
A clock is being constructed using the Label Widget, which exhibits the current time and is positioned using grid. 
'''
clock = tk.Label(window, font=("times", 90, "bold"), bg="blue", fg='white')
clock.grid(row=2, column=2, padx=620, pady=250)

'''

calling the function here
'''
clocks()

'''
running the main window
'''
if __name__ == "__main__":

    window.mainloop()
