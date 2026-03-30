alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
         'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']

def gcd(a, b):               # PGCD  
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):      #  Inverse mod(m)
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return 0

def affine_encryption(text, a, b):
    if a <= 0 or gcd(a, len(alphabet)) != 1:
        raise ValueError("a must be greater than 0 and prime with the length of the alphabet.")
    else:
        result = ""
        for i in text:
            if i in alphabet:
                result += alphabet[(a * alphabet.index(i) + b) % len(alphabet)]
        return result

def affine_decryption(text, a, b):
    if a <= 0 or gcd(a, len(alphabet)) != 1:
        raise ValueError("a must be greater than 0 and prime with the length of the alphabet.")
    else:
        result = ""
        a_inv = mod_inverse(a, len(alphabet))
        if a_inv == 0:
            raise ValueError("Inverse does not exist. a and the length of the alphabet must be coprime.")
        for i in text:
            if i in alphabet:
                result += alphabet[(a_inv * (alphabet.index(i) - b)) % len(alphabet)]
        return result