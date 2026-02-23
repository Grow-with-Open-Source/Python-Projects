import hashlib

def sha256_enc(message: str):

    return hashlib.sha256(message.encode()).hexdigest()