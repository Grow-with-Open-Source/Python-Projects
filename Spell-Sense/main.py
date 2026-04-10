import tkinter as tk
from logic import get_correction

class SpellCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spell Checker Pro")
        self.root.geometry("400x300")
        self.root.configure(bg='#f7f7f7')
        
        self.setup_ui()
        self.root.bind('<Return>', lambda e: self.process_text())

    def setup_ui(self):
        # Label
        tk.Label(self.root, text="Pro Spell Checker", font=("Arial", 14, "bold"), bg='#f7f7f7').pack(pady=10)
        
        # Entry
        self.input_entry = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.input_entry.pack(pady=10)
        self.input_entry.focus_set()

        # Buttons
        btn_frame = tk.Frame(self.root, bg='#f7f7f7')
        btn_frame.pack(pady=10)

        self.check_btn = tk.Button(btn_frame, text="Check", command=self.process_text, bg='#4CAF50', fg='white', width=10)
        self.check_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset_fields, bg='#f44336', fg='white', width=10)
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        # Result display
        self.result_label = tk.Label(self.root, text="", font=("Arial", 11), bg='#f7f7f7', wraplength=350)
        self.result_label.pack(pady=20)

    def process_text(self):
        text = self.input_entry.get()
        corrected, is_correct = get_correction(text)

        if corrected is None:
            self.result_label.config(text="Please enter a word!", fg="orange")
        elif is_correct:
            self.result_label.config(text=f"✔ '{text}' is spelled correctly!", fg="green")
        else:
            self.result_label.config(text=f"✖ Suggestion: {corrected}", fg="blue")

    def reset_fields(self):
        self.input_entry.delete(0, tk.END)
        self.result_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpellCheckerApp(root)
    root.mainloop()