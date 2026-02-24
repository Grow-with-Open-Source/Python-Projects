# Let's start with Hashes! (more specifically SHA256)
# Hashes are a way to encrypt thing in a irreversible way
# This means if you encrypt something using Hash Methods there is no way to know the content

# In this example we using pre-installed module called "hashlib"

import hashlib

def encryption_sha(message: str):
    return hashlib.sha256().digest() # This makes the encryption in SHA-256. This is the usually how your passkeys are encrypted
