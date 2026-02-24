from encryption import sha, aes, base64
import os

def main(): 
    while True:
        print("""Welcome to Encryption Project\n
              1 - SHA256\n
              2 - AES\n
              3 - Base64\n
              4 - Quit\n
              More soon!\n""")

        encrypt_choice = int(input())

        match encrypt_choice:
            case 1:
                message_to_encrypt = input("What's the message you want to encrypt?: ")

                encrypted_message = sha.encryption_sha(message_to_encrypt)

                print(f"The encrypted message is: {encrypted_message}")

            case 2:
                aes_choice = int(input("1 - Encrypt\n2 - Decrypt\n"))   

                if aes_choice == 1:
                    message_to_encrypt = input("What's the message you want to encrypt? ").encode('utf-8')
                    key = os.urandom(16) # if you are confused, this just guarantee the key will have 16 bytes

                    encrypted_message, nonce = aes.encrypt_aes(message_to_encrypt, key)

                    print(f"Encrypted message: {encrypted_message}\nnonce: {nonce}\nkey: {key}\n *Save those!*")
                elif aes_choice == 2:
                    message_to_decrypt = eval(input("What's the message to decrypt? "))
                    key = eval(input("What's the key? "))
                    nonce = eval(input("What's the nonce? "))

                    decrypted_message = aes.decrypt_aes(message_to_decrypt, key, nonce)

                    print(f"Message: {decrypted_message}")
                
                else:
                    print("Option does not exist")
            
            case 3:
                base_choice = int(input("1 - Encrypt\n2 - Decrypt\n"))  

                if base_choice == 1:
                    message_to_encrypt = input("What's the message you want to encrypt? ")

                    encrypted_message = base64.encrypt_base64(message_to_encrypt)

                    print(f"Message: {encrypted_message}")

                elif base_choice == 2:
                    message_to_decrypt = input("What's the message to decrypt? ")

                    decrypted_message = base64.decrypt_base64(message_to_decrypt)

                    print(f"Message: {decrypted_message}")
                
                else:
                    print("Option does not exist")
            
            case 4:
                print("Bye!")
                break
        
            case _:
                print("This option is not available")

if __name__ == "__main__":
    main()
