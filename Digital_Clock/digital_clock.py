from tkinter import Tk, Label
from tkinter.font import Font
import time


class DigitalClock:
    def __init__(self, font=None):
        """Initialize the digital clock."""
        self.create_window()
        self.configure_window()
        self.set_font(font)
        self.add_header()
        self.add_clock()
        self.add_date()  # ✅ Added new method to show date
        self.update_time_on_clock()

    def create_window(self):
        """Create the main window."""
        self.window = Tk()

    def configure_window(self):
        """Configure the main window properties."""
        self.window.title('Digital Clock')
        self.window.config(bg='black')

    def set_font(self, customFont):
        """Set the font for the clock display."""
        DEFAULT_FONT = Font(family='Arial', size=90, weight='normal')
        self.font = customFont if customFont is not None else DEFAULT_FONT

    def add_header(self):
        """Add a header label to the window."""
        self.header = Label(self.window, text='Time Clock',
                            font=self.font, bg='gray', fg='white')
        self.header.grid(row=1, column=2)

    def add_clock(self):
        """Add the clock label to the window."""
        self.clock = Label(self.window, font=(
            'times', 90, 'bold'), bg='blue', fg='white')
        self.clock.grid(row=2, column=2, padx=620, pady=250)

    def add_date(self):
        """Add a date label below the clock."""
        self.date_label = Label(self.window, font=('times', 40, 'bold'), bg='black', fg='white')
        self.date_label.grid(row=3, column=2)
        self.update_date_on_clock()

    def update_date_on_clock(self):
        """Update the date displayed below the clock."""
        currentDate = time.strftime("%d-%b-%Y")
        self.date_label.config(text=currentDate)
        # Update every midnight (24*60*60*1000 ms)
        self.date_label.after(86400000, self.update_date_on_clock)

    def update_time_on_clock(self):
        """Update the time displayed on the clock every second."""
        currentTime = time.strftime("%H:%M:%S")
        self.clock.config(text=currentTime)
        self.clock.after(1000, self.update_time_on_clock)

    def start(self):
        """Start the Tkinter main loop."""
        self.window.mainloop()


if __name__ == "__main__":
    clock = DigitalClock()
    clock.start()
