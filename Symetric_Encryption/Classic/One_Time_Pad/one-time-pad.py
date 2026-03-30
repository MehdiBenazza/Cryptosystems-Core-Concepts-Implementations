# Masque jetable (One-time pad)
# vigenere avec un cle aleatoire de la meme longueur que le message
import random
import Vigenere

def generate_random_key(length):
    characters = Vigenere.alphabet
    key = ''.join(random.choice(characters) for i in range(length))
    return key

def encrypt_otp(text, key):
    return Vigenere.vigenere_encryption(text, key)

def decrypt_otp(ciphertext, key):
    return Vigenere.vigenere_decryption(ciphertext, key)