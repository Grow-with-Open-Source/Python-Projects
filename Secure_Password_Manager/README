# 🔐 Secure Password Manager (CLI + GUI)

This is a simple and secure Password Manager built with Python. It includes both a **Tkinter-based GUI (Graphical User Interface)** and a **CLI (Command Line Interface)** version.

---

## 📌 Features

* ✅ Generate strong, random passwords
* ✅ Choose what characters to include (lowercase, uppercase, digits, special characters)
* ✅ Real-time password strength feedback
* ✅ Save passwords with labels (e.g., Gmail, Netflix)
* ✅ Encode/Encrypt passwords for security
* ✅ View saved passwords with automatic decryption
* ✅ GUI built using Python's `tkinter` library
* ✅ CLI version with command-line options using `argparse`

---

## 💡 How It Works

### Tkinter GUI

The graphical interface is built using `tkinter`, Python’s standard GUI toolkit. It provides a clean interface for generating, encrypting, and viewing passwords.

### Generate Password

1. Choose the password length.
2. Select character types using checkboxes.
3. Hit the **Generate Password** button.
4. The password is displayed with its strength (Weak, Medium, or Strong).
5. The password is then **encrypted** and saved to a file.

### View Saved Passwords

1. Click the **View Saved Passwords** button in the GUI.
2. If the encryption key exists, the program decrypts and displays all saved passwords in a pop-up window.
3. If the key is missing or corrupted, an error message is shown.

---

## 🛠️ Technologies Used

| Component | Tool/Library |
|----------|--------------|
| Programming Language | Python |
| GUI Library | Tkinter |
| Encryption | cryptography (Fernet) |
| Encoding (CLI version) | base64 |
| CLI Parser | argparse |
| Version Control | Git |

---

## 🗃️ Project Structure

```bash
Password_Manager/
├── password_manager_gui.py       # Tkinter-based GUI application
├── password_manager_cli.py       # CLI-based password generator
├── view_passwords_cli.py         # View decoded Base64 passwords (CLI)
├── decrypt_passwords_cli.py      # Decrypt encrypted passwords (CLI)
├── saved_passwords.txt           # File where encrypted passwords are saved
├── secret.key                    # File containing Fernet encryption key
├── README.md
└── .gitignore
```

---

## ⚠️ Security Note

This project uses **Fernet encryption** to protect your saved passwords.

Files like `secret.key` and `saved_passwords.txt` are excluded from version control using `.gitignore`.

> Do not share your `secret.key` with anyone. If you lose it, saved passwords cannot be decrypted.

---

## 🧠 Ideal For

- Python beginners learning `tkinter`
- Students building secure Python projects
- Learning encryption basics with `cryptography`
- Practicing Git and GitHub workflow with versioned features

---

## ⚙️ Setup Instructions

1. Clone the repo  
   `git clone https://github.com/Your-Username/Secure_Password_Manager.git`

2. Install dependencies  
   `pip install cryptography`

3. Run GUI  
   `python password_manager_gui.py`

4. Or use CLI  
   `python password_manager_cli.py --length 12 --label Gmail --lower --upper --digits --specials`

---

## ⭐ GitHub Ready

This project was built using proper Git practices:

* Every feature added on a new branch
* Meaningful commit messages
* Clean merge history

---
