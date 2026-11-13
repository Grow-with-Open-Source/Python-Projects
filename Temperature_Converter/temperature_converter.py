from tkinter import *
window = Tk()
window.title("temperature_converter")
def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def celsius_to_kelvin(celsius):
    return celsius + 273.15


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def fahrenheit_to_kelvin(fahrenheit):
    return (fahrenheit - 32) * 5 / 9 + 273.15


def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9 / 5 + 32

def ctf():
    inp = entry.get()
    finp = float(inp)
    entry.delete(0, END)
    entry.insert(0,celsius_to_fahrenheit(finp))
def ftc():
    inp = entry.get()
    finp = float(inp)
    entry.delete(0, END)
    entry.insert(0,fahrenheit_to_celsius(finp))
def ctk():
    inp = entry.get()
    finp = float(inp)
    entry.delete(0, END)
    entry.insert(0,celsius_to_kelvin(finp))
def ktc():
    inp = entry.get()
    finp = float(inp)
    entry.delete(0, END)
    entry.insert(0,kelvin_to_celsius(finp))
def ftk():
    inp = entry.get()
    finp = float(inp)
    entry.delete(0, END)
    entry.insert(0,fahrenheit_to_kelvin(finp))
def ktf():
    inp = entry.get()
    finp = float(inp)
    entry.delete(0, END)
    entry.insert(0,kelvin_to_fahrenheit(finp))
           

entry = Entry(window,bg="gray",fg="black",font="bold")
button1 = Button(window,bg="black",fg="white",font="bold",text="C t F",width=20,command=ctf)
button2 = Button(window,bg="black",fg="white",font="bold",text="F t C",width=20,command=ftc)
button3 = Button(window,bg="black",fg="white",font="bold",text="C t K",width=20,command=ctk)
button4 = Button(window,bg="black",fg="white",font="bold",text="K t C",width=20,command=ktc)
button5 = Button(window,bg="black",fg="white",font="bold",text="F t K",width=20,command=ftk)
button6 = Button(window,bg="black",fg="white",font="bold",text="K t F",width=20,command=ktf)
entry.pack(padx=50,pady=50)
button1.pack(side="left")
button2.pack(side="left")
button3.pack(side="left")
button4.pack(side="left")
button5.pack(side="left")
button6.pack(side="left")

window.mainloop()