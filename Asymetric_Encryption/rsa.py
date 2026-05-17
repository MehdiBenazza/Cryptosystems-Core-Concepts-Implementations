import random
from math import gcd

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_random_prime_nbr(n):
    """Generate a random prime number smaller than n"""
    while True:
        p = random.randint(2, n - 1)
        if is_prime(p):
            return p

def mod_inverse(a, m):
    m0 = m
    y = 0
    x = 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x += m0
    return x
        
def rsa_encrypt(text):
    p = generate_random_prime_nbr(100)
    q = generate_random_prime_nbr(100)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = random.randint(2, phi_n - 1)
    while gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)

    d = mod_inverse(e, phi_n)

    encrypted_text = [pow(ord(char), e, n) for char in text]
    
    return encrypted_text, (e, n), (d, n)

def rsa_decrypt(encrypted_text, private_key):
    d, n = private_key
    decrypted_text = ''.join([chr(pow(char, d, n)) for char in encrypted_text])
    return decrypted_text

if __name__ == "__main__":
    text = input("Enter the text to encrypt: ")
    encrypted_text, public_key, private_key = rsa_encrypt(text)
    print(f"Encrypted text: {encrypted_text}")
    decrypted_text = rsa_decrypt(encrypted_text, private_key)
    print(f"Decrypted text: {decrypted_text}")