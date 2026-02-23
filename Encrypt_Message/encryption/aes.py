from Crypto.Cipher import AES

def aes_enc(message: str, key: bytes):
    mess = message.encode()
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    mess_cipher, tag = cipher.encrypt_and_digest(mess)
    return mess_cipher, nonce

def aes_desc(message: bytes, key: bytes, nonce: bytes):
    
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(message)