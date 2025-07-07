import base64

def view_passwords(filename="saved_passwords.txt"):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        # Temperory variable to store each password block info
        timestamp = label = encoded_password = ""
        included_options = ""

        print("\n🔐 Saved Passwords:\n")

        for line in lines:
            line = line.strip()

            if line.startswith("["): # Timestamp line
                timestamp = line.strip("[]")

            elif line.startswith("Label:"):
                label = line.split("Label:")[1].strip()

            elif line.startswith("Encoded Password:"):
                encoded_password = line.split("Encoded Password:")[1].strip()
                try:
                    decoded_password = base64.b64decode(encoded_password.encode()).decode()
                except Exception as e:
                    decoded_password = f"[Error decoding password: {e}]"

            elif line.startswith("Included"):
                included_options = line.split("Included -")[1].strip()

            elif line.startswith("-" * 10): # Block ends here
                print(f"📅 Date/Time: {timestamp}")
                print(f"🏷️ Label: {label}")
                print(f"🔓 Decoded Password: {decoded_password}")
                print(f"🔧 Options Included: {included_options}")
                print("-" * 40)

    except FileNotFoundError:
        print("❌ saved_passwords.txt not found.")

    except Exception as e:
        print(f"❌ An error occured: {e}")

# Run the function
if __name__ == '__main__':
    view_passwords()