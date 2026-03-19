# Let's start
# Base64 is NOT a safe way to encrypt important things, it's used to encrypt binary data to text and doesn't have a key such as AES
# If you pretend encrypting something that you need to know later you should use AES
# Else you just want to encrypt something and doesn't care about the privacy Base64 might be a good choice

# In this example we are using a pre-installed module from Python called "base64"

import base64

def encrypt_base64(message: str):
    encrypt_message = base64.b64encode(message.encode()).decode()
    return encrypt_message

def decrypt_base64(message: str):
    decrypt_message = base64.b64decode(message).decode('utf-8')
    return decrypt_message