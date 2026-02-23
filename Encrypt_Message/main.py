from encryption import sha, aes
import os

def main():
    """
    This is the entry point of this Encryption Message
    """

    print("""Welcome to Encrypt Message!\n
          Your options are:\n
          1 - AES\n
          2 - SHA\n
""")
    
    option = int(input())

    match option:
        case 1:

            print("""Do you want to encrypt or decrypt a message?\n
                  1 - Encrypt
                  2 - Decrypt""")

            enc_dec = int(input())

            if enc_dec == 1:

                message = input("Which message you want to encrypt? ")
                key = os.urandom(16)

                print(f"Your key is {key}\n*Save it!*")

                enc_mess, nonce = aes.aes_enc(message, key)

                print(f"{enc_mess}\n{nonce}\n*Save this*")
            else:
                message = eval(input("What's the message you want to decrypt? "))
                key = eval(input("What's the key? "))
                nonce = eval(input("What's the nonce? "))

                desc_mess = aes.aes_desc(message, key, nonce)

                print(f"{desc_mess}")

        case 2:
            message = input("What's the message you want to hide? (This method is unreversible)")

            enc_mess = sha.sha256_enc(message)

            print(f"{enc_mess}")

if __name__ == "__main__":
    main()

