import random, datetime, base64, argparse, os
from cryptography.fernet import Fernet

# 🔑 File where secret key will be stored
KEY_FILE = "secret.key"

# ------------------------------------------------------
# STEP 1: Generate a new encryption key (only once))
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

# STEP 2: Load the ecryption key
def load_key():
    if not os.path.exists(KEY_FILE):
        print("No Key found. Creating a new one...")
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

# STEP 3: Generate password based on user settings
def generate_password(length, use_lower, use_upper, use_digits, use_specials):
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    specials = '!@#$%^&*()'

    # Build character set based on user input
    character_set = ''
    
    if use_lower:
        character_set = character_set + lowercase
    if use_upper:
        character_set = character_set + uppercase
    if use_digits:
        character_set = character_set + digits
    if use_specials:
        character_set = character_set + specials

    if not character_set:
        return "Error: No character sets selected. Cannot generate password."

    password = ''
    for i in range(length):
        password = password + random.choice(character_set)
    return password

# STEP 4: Check password strength
def check_strength(length, use_lower, use_upper, use_digits, use_specials):
    score = 0

    # Add points for character variety
    score = score + use_lower + use_upper + use_digits + use_specials

    if length >= 12:
        score = score + 1

    if score <= 2:
        return "Weak"
    elif score == 3 or score == 4:
        return "Medium"
    else:
        return "Strong"
    
# STEP 5: Command-line interface using argparse
def main():
    parser = argparse.ArgumentParser(description="🔐 Password Generator Tool")

    parser.add_argument('--length', type=int, required=True, help='Password length (e.g., 8, 12, 16)')
    parser.add_argument('--label', type=str, required=True, help='Purpose or label for the password (e.g, Google, Gmail)')
    parser.add_argument('--lower', action='store_true', help='Include lowercase letters')
    parser.add_argument('--upper', action='store_true', help='Include uppercase letters')
    parser.add_argument('--digits', action='store_true', help='Include digits')
    parser.add_argument('--specials', action='store_true', help='Include special characters')

    args = parser.parse_args()

    # Validate length
    if args.length <= 0:
        print("❌ Password length must be positive. Try again.")
        return
    
    # Generate and evaluate password
    password = generate_password(args.length, args.lower, args.upper, args.digits, args.specials)
    if password.startswith("Error"):
        print(password)
        return
    
    print(f"✅ Your generated password is: {password}")
    strength = check_strength(args.length, args.lower, args.upper, args.digits, args.specials)
    print(f"💪 Password Strenght: {strength}")

    # STEP 6: Encrypt password using Fernet
    key = load_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode()).decode() # This variable already holds the Fernet encrypted string.

    # STEP 7: Save encrypted password to file
    with open("saved_passwords.txt", "a") as file:
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        # The 'encoded_password' (base64 of original password) was being saved previously.
        # We should save the 'encrypted_password' (Fernet encrypted string) instead.
        file.write(f"\n[{timestamp}]\n")
        file.write(f"Label: {args.label}\n")
        file.write(f"Encrypted Password: {encrypted_password}\n") # Save the Fernet encrypted password and use "Encrypted Password:" label
        file.write(f"Included - Lowercase: {args.lower}, Uppercase: {args.upper}, Digits: {args.digits}, Special Characters: {args.specials}\n")
        file.write("-" * 40 + "\n")

    print("🔒 Password encrypted and saved to 'saved_passwords.txt")


if __name__ == '__main__':
    main()