from cryptography import fernet
import os

KEY_FILE = "secret.key"
PASSWORD_FILE = "saved_passwords.txt"

# STEP 1: Load the encryption key
def load_key():
    if not os.path.exists(KEY_FILE):
        print("❌ Encryption key not found. Cannot decrypt passwords.")
        return None
    with open(KEY_FILE, "rb") as f:
        return f.read()
    
# STEP 2: Decrypt the passwords
def decrypt_password(encrypted_text, fernet_cipher_suite): # Renamed parameter for clarity
    try:
        return fernet_cipher_suite.decrypt(encrypted_text.encode()).decode()
    except Exception:
        return "[Decryption Failed]"
    
# STEP 3: Read and decrypt all entries
def view_passwords():
    if not os.path.exists(PASSWORD_FILE):
        print("❌ No saved passwords found")
        return
    
    key = load_key()
    if not key:
        return
    
    # Fernet = fernet(key) # Original line causing TypeError
    active_fernet_cipher = fernet.Fernet(key) # Correctly instantiate Fernet class from the module

    print("🔐 Saved Encrypted Passwords\n" + "=" * 40)
    with open(PASSWORD_FILE, "r") as file:
        lines = file.readlines()

        current_block = {}

        for line in lines:
            line = line.strip()

            if line.startswith("[") and "]" in line:
                current_block["timestamp"] = line.strip("[]")
            elif line.startswith("Label:"):
                current_block["label"] = line.split("Label:")[1].strip()
            elif line.startswith("Encrypted Password:"):
                current_block["encrypted"] = line.split("Encrypted Password:")[1].strip()
            elif line.startswith("Included -"):
                current_block["options"] = line.split("Included -")[1].strip()
            elif line.startswith("-" * 10):
             # print everything together
                print(f"\n📅 Date/Time: {current_block.get('timestamp', '[Unknown]')}")
                print(f"🏷️  Label: {current_block.get('label', '[None]')}")
                print(f"🔓 Password: {decrypt_password(current_block.get('encrypted', ''), active_fernet_cipher)}") # Pass the Fernet instance
                print(f"⚙️  Options: {current_block.get('options', '[Not specified]')}")
                print("-" * 40)
                current_block = {}  # Reset for next block

# STEP 4: Entry point
if __name__ == '__main__':
    view_passwords()