import tkinter as tk
from textblob import TextBlob

def check_spelling():
    input_text = input_entry.get()
    corrected_text = TextBlob(input_text).correct()
    result_label.config(text="Corrected text: " + str(corrected_text))

def reset():
    input_entry.delete(0, tk.END)
    result_label.config(text="Corrected text: ")

root = tk.Tk()
root.title("Spell Checker")

# Increase window size
root.geometry("400x200")

# Configure background color
root.configure(bg='#f0f0f0')

input_label = tk.Label(root, text="Enter the word to be checked:", bg='#f0f0f0')
input_label.pack(pady=10)

input_entry = tk.Entry(root)
input_entry.pack(pady=5)

check_button = tk.Button(root, text="Check Spelling", command=check_spelling, bg='#4CAF50', fg='white')
check_button.pack(pady=10)

result_label = tk.Label(root, text="Corrected text: ", bg='#f0f0f0')
result_label.pack(pady=5)

reset_button = tk.Button(root, text="Reset", command=reset, bg='#f44336', fg='white')
reset_button.pack(pady=10)

root.mainloop()