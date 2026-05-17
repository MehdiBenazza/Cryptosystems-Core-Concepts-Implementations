alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
         'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']

def cesar_encryption(text, shift):
    result = ""
    for i in text:
        if i in alphabet:
            result += alphabet[(alphabet.index(i) + shift) % len(alphabet)]
    return result

def cesar_decryption(text, shift):
    result = ""
    for i in text:
        if i in alphabet:
            result += alphabet[(alphabet.index(i) - shift) % len(alphabet)]
    return result

def main():
    while True:
        print("===== Cesar =====")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            text = input("Enter the plaintext: ")
            shift = int(input("Enter the shift value: "))
            encrypted_text = cesar_encryption(text, shift)
            print(f"Encrypted text: {encrypted_text}")
        
        elif choice == 2:
            text = input("Enter the ciphertext: ")
            shift = int(input("Enter the shift value: "))
            decrypted_text = cesar_decryption(text, shift)
            print(f"Decrypted text: {decrypted_text}")
        
        else:
            break