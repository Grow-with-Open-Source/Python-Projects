import secrets
import string

def generate_password(length: int = 12, digits: bool = True, symbols: bool = True) -> str:
    
    min_required = int(digits) + int(symbols)
    if length < min_required:
        raise ValueError("Password length too small for selected options")
    
    pool = string.ascii_letters
    required_chars = []
    
    if digits:
        pool += string.digits
        required_chars.append(secrets.choice(string.digits))

    if symbols:
        pool += string.punctuation
        required_chars.append(secrets.choice(string.punctuation))
    
    remaining_length = length - len(required_chars)
    
    password = required_chars + [secrets.choice(pool) for _ in range(remaining_length)]
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)

def save(passwords: list) -> None:
    try:
        agree: str = input("Do you want to save the passwords to a file? (y/n): ").lower().strip()
        if agree not in ["y", "yes"]:
            return
        else:
            fileName: str = input("Enter the name of the file (without .txt): ").strip()
            if not fileName:
                fileName: str = "passwords"
        print("\nSaving passwords to file...")
        with open(fileName + ".txt", "w") as f:
            for password in passwords:
                f.write(password + "\n")
        print("Passwords saved successfully!")
    except OSError as e:
        print(f"Error saving passwords: {e}")

def main():
    try:
        length: int = int(input("Enter the length of the password: "))
        count: int = int(input("Enter the number of passwords to generate: "))
        
        if length < 1 or count < 1:
            print("Please enter positive integers only.")
            return
        
        if length > 128:
            print("Password length cannot be greater than 128 characters.")
            return
        
        if length < 6:
            print("Password is too short - Generating Passwords of length 6")
            length = 6
        
        digits: bool = input("Include digits? (y/n): ").lower().strip() in ["y", "yes"]
        symbols: bool = input("Include symbols? (y/n): ").lower().strip() in ["y", "yes"]
        
        print("\nGenerating Secure Passwords...\n")
        passwords = []
        for i in range(count):
            password = generate_password(length, digits=digits, symbols=symbols)
            passwords.append(password)
            print(f"Password #{i + 1}: {password}")
        
        save(passwords)
        
    except ValueError:
        print("Please Enter Valid Integers Only")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()