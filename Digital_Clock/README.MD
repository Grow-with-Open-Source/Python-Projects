# Digital Clock

A simple Python-based digital clock application with a graphical user interface built using `Tkinter`. This project displays the current time in real-time and is designed to be visually appealing, lightweight, and customizable.

---

## Features

- **Real-Time Clock Display:**  
  Displays the current time in `HH:MM:SS` format and updates every second.

- **Customizable Design:**  
  Easily modify the clock’s font, colors, and layout to suit your preferences.

- **Header Label:**  
  Includes a "Time Clock" header for a professional and organized look.

- **User-Friendly Interface:**  
  The application features a clean and vibrant design for an engaging user experience.

- **Lightweight and Fast:**  
  Built with `Tkinter`, the application runs efficiently without consuming significant system resources.

---

## How It Works

1. **Initialization:**  
   The `DigitalClock` class sets up the main window, configures its appearance, and initializes the clock and header.

2. **Real-Time Updates:**  
   The `update_time_on_clock` method retrieves the current system time and updates the clock display every second using `Tkinter`'s `after()` method.

3. **Execution:**  
   The application runs continuously, keeping the time accurate until the user closes the window.


