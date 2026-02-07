from tkinter import Tk, Label, Entry, Button, messagebox
from tkinter.font import Font
import time
from tkinter import Checkbutton, BooleanVar
from tkinter import Canvas



class DigitalClock:
    def __init__(self, font=None):
        """Initialize the digital clock."""
        self.create_window()
        self.configure_window()
        self.is_dark = True
        self.set_font(font)
        self.add_header()
        self.add_clock()
        self.add_date()  # ✅ Added new method to show date
        self.add_theme_button()
        # self.add_theme_toggle()
        self.is_24_hour = True
        self.alarm_time = None
        self.add_format_toggle()
        self.add_alarm_section()
        self.update_time_on_clock()

    def add_format_toggle(self):
        self.format_button = Button(self.window,
                                    text="Switch to 12 Hour",
                                    font=("times", 15, "bold"),
                                    command=self.toggle_format)
        self.format_button.grid(row=5, column=2, pady=5)

    def toggle_format(self):
        if self.is_24_hour:
            self.is_24_hour = False
            self.format_button.config(text="Switch to 24 Hour")
        else:
            self.is_24_hour = True
            self.format_button.config(text="Switch to 12 Hour")

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
        self.clock.grid(row=2, column=2, padx=500, pady=100)
        # self.clock.grid(row=2, column=2, pady=20)

    def add_date(self):
        """Add a date label below the clock."""
        self.date_label = Label(self.window, font=('times', 40, 'bold'), bg='black', fg='white')
        self.date_label.grid(row=3, column=2)
        self.update_date_on_clock()

    # def toggle_theme(self):
    #     if self.is_dark:
    #         self.window.config(bg="white")
    #         self.clock.config(bg="white", fg="black")
    #         self.date_label.config(bg="white", fg="black")
    #         self.header.config(bg="lightgray", fg="black")
    #     else:
    #         self.window.config(bg="black")
    #         self.clock.config(bg="black", fg="white")
    #         self.date_label.config(bg="black", fg="white")
    #         self.header.config(bg="gray", fg="white")

    #     self.is_dark = not self.is_dark

    def toggle_theme(self):
        if self.theme_var.get():   # Dark mode ON
            self.window.config(bg="black")
            self.clock.config(bg="black", fg="white")
            self.date_label.config(bg="black", fg="white")
            self.header.config(bg="gray", fg="white")
            self.theme_toggle.config(bg="black", fg="white")
        else:   # Light mode
            self.window.config(bg="white")
            self.clock.config(bg="white", fg="black")
            self.date_label.config(bg="white", fg="black")
            self.header.config(bg="lightgray", fg="black")
            self.theme_toggle.config(bg="white", fg="black")

    # def add_theme_button(self):
    #     self.theme_button = Label(self.window, text="Toggle Theme",
    #                             font=("times", 20, "bold"),
    #                             bg="green", fg="white",
    #                             cursor="hand2")
    #     self.theme_button.grid(row=4, column=2)
    #     self.theme_button.bind("<Button-1>", lambda e: self.toggle_theme())

    def add_theme_button(self):
        self.theme_var = BooleanVar(value=True)

        self.theme_toggle = Checkbutton(
            self.window,
            text="Dark Mode",
            variable=self.theme_var,
            command=self.toggle_theme,
            bg="black",
            fg="white",
            selectcolor="black",
            font=("times", 15, "bold")
        )

        self.theme_toggle.grid(row=4, column=2, pady=10)

    def update_date_on_clock(self):
        """Update the date displayed below the clock."""
        currentDate = time.strftime("%d-%b-%Y")
        self.date_label.config(text=currentDate)
        # Update every midnight (24*60*60*1000 ms)
        self.date_label.after(86400000, self.update_date_on_clock)

    def update_time_on_clock(self):
        """Update the time displayed on the clock every second."""
        # currentTime = time.strftime("%H:%M:%S")
        
        if self.is_24_hour:
            currentTime = time.strftime("%H:%M:%S")
        else:
            currentTime = time.strftime("%I:%M:%S %p")
        
        if self.alarm_time == currentTime:
            messagebox.showinfo("Alarm", "⏰ Time's Up!")
            self.alarm_time = None

        self.clock.config(text=currentTime)
        self.clock.after(1000, self.update_time_on_clock)

    def start(self):
        """Start the Tkinter main loop."""
        self.window.mainloop()
    
    def add_alarm_section(self):
        self.alarm_entry = Entry(self.window, font=("times", 15))
        self.alarm_entry.grid(row=6, column=2, pady=5)

        self.alarm_button = Button(self.window,
                                    text="Set Alarm (HH:MM:SS)",
                                    font=("times", 12, "bold"),
                                    command=self.set_alarm)
        self.alarm_button.grid(row=7, column=2, pady=5)

    def set_alarm(self):
        alarm_input = self.alarm_entry.get()

        try:
            time.strptime(alarm_input, "%H:%M:%S")
            self.alarm_time = alarm_input
            messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_input}")
        except ValueError:
            messagebox.showerror("Invalid Format", "Use HH:MM:SS format")

 


if __name__ == "__main__":
    clock = DigitalClock()
    clock.start()