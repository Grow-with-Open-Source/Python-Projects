# Let's start with AES
# AES is a type of encryption used mainly for things that require certain level of safety and later will be used
# There is a specific thing you shouldn't encrypt with AES that's Passkeys
# For passkeys you will use a method showed later that are the Hash Methods

# In this example we using pycryptodome

from Crypto.Cipher import AES

def encrypt_aes(message: str, key: str):
    encrypt_cipher = AES.new(key, AES.MODE_EAX) # This is the "configuration" for the encryption

    nonce = encrypt_cipher.nonce # Nonce aka Number Once is basically what makes the key random

    encrypted_message = encrypt_cipher.encrypt_and_digest(message) # Here we are truly encrypting the message

    return encrypted_message, nonce

def decrypt_aes(message: bytes, key: bytes, nonce: bytes):
    decrypt_cipher = AES.new(key, AES.MODE_EAX, nonce=nonce) # Here we are Saying what's the key, type of encryption and nonce
    decrypted_message = decrypt_cipher.decrypt(message)
    return decrypted_message
