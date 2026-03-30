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