# Masque jetable (One-time pad)
# vigenere avec un cle aleatoire de la meme longueur que le message
import random
from ..Vigenere.vigenere import alphabet, vigenere_encryption, vigenere_decryption

def generate_random_key(length):
    characters = alphabet
    key = ''.join(random.choice(characters) for i in range(length))
    return key

def encrypt_otp(text):
    key = generate_random_key(len(text))

    return vigenere_encryption(text, key)

def decrypt_otp(ciphertext, key):
    return vigenere_decryption(ciphertext, key)

def main():
    while True:
        print("===== One-Time Pad =====")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            text = input("Enter the plaintext: ")
            encrypted_text = encrypt_otp(text)
            print(f"Encrypted text: {encrypted_text}")
        
        elif choice == 2:
            ciphertext = input("Enter the ciphertext: ")
            key = input("Enter the key: ")
            decrypted_text = decrypt_otp(ciphertext, key)
            print(f"Decrypted text: {decrypted_text}")
        
        else:
            break