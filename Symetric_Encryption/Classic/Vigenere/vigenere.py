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