alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
         'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']

def vigenere_encryption(text, key):
    result = ""
    key_length = len(key)
    for i in range(len(text)):
        if text[i] in alphabet:
            shift = alphabet.index(key[i % key_length])
            result += alphabet[(alphabet.index(text[i]) + shift) % len(alphabet)]
    return result

def vigenere_decryption(text, key):
    result = ""
    key_length = len(key)
    for i in range(len(text)):
        if text[i] in alphabet:
            shift = alphabet.index(key[i % key_length])
            result += alphabet[(alphabet.index(text[i]) - shift) % len(alphabet)]
    return result

def main():
    while True:
        print("===== Vigenere =====")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            text = input("Enter the plaintext: ")
            key = input("Enter the key: ")
            encrypted_text = vigenere_encryption(text, key)
            print(f"Encrypted text: {encrypted_text}")
        
        elif choice == 2:
            text = input("Enter the ciphertext: ")
            key = input("Enter the key: ")
            decrypted_text = vigenere_decryption(text, key)
            print(f"Decrypted text: {decrypted_text}")
        
        else:
            break