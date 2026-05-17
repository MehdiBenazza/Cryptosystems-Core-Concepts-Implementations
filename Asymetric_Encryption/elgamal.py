import random
from math import gcd


# ─────────────────────────────────────────────
#  Utilitaires communs
# ─────────────────────────────────────────────

def is_prime(n):
    """Teste si n est un nombre premier."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def generate_random_prime(n):
    """Génère un nombre premier aléatoire inférieur à n."""
    while True:
        p = random.randint(2, n - 1)
        if is_prime(p):
            return p


def generate_large_prime(bits=10):
    """Génère un nombre premier aléatoire d'environ `bits` bits."""
    lower = 2 ** (bits - 1)
    upper = 2 ** bits - 1
    while True:
        p = random.randint(lower, upper)
        if is_prime(p):
            return p


def find_primitive_root(p):
    """Trouve une racine primitive (générateur) de Zp*."""
    if p == 2:
        return 1
    phi = p - 1
    # Facteurs premiers de phi
    factors = prime_factors(phi)
    for g in range(2, p):
        ok = True
        for factor in factors:
            if pow(g, phi // factor, p) == 1:
                ok = False
                break
        if ok:
            return g
    return None


def prime_factors(n):
    """Retourne l'ensemble des facteurs premiers de n."""
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors


def mod_inverse(a, m):
    """Inverse modulaire de a mod m (algorithme d'Euclide étendu)."""
    m0, y, x = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        a, m = m, a % m
        x, y = y, x - q * y
    return x + m0 if x < 0 else x


def elgamal_generate_keys(bits=10):
    """
    Génère une paire de clés ElGamal.
      Clé publique  : (p, g, h)   avec h = g^x mod p
      Clé privée    : (p, x)
    """
    p = generate_large_prime(bits)
    g = find_primitive_root(p)

    # Clé privée x ∈ ]1, p-1[
    x = random.randint(2, p - 2)

    # Clé publique h = g^x mod p
    h = pow(g, x, p)

    public_key  = (p, g, h)
    private_key = (p, x)
    return public_key, private_key


def elgamal_encrypt(text, public_key):
    """
    Chiffre un texte caractère par caractère avec ElGamal.
    Pour chaque caractère m :
      - Choisit un k aléatoire dans ]1, p-1[
      - c1 = g^k mod p
      - c2 = m * h^k mod p
    Retourne une liste de paires (c1, c2).
    """
    p, g, h = public_key
    encrypted = []
    for char in text:
        m = ord(char)
        if m >= p:
            raise ValueError(
                f"Le caractère '{char}' (ord={m}) dépasse p={p}. "
                "Augmentez le paramètre `bits` de generate_keys."
            )
        k  = random.randint(2, p - 2)
        c1 = pow(g, k, p)
        c2 = (m * pow(h, k, p)) % p
        encrypted.append((c1, c2))
    return encrypted


def elgamal_decrypt(encrypted_text, private_key):
    """
    Déchiffre un texte chiffré ElGamal.
    Pour chaque paire (c1, c2) :
      m = c2 * (c1^x)^(-1) mod p
    """
    p, x = private_key
    decrypted = ""
    for c1, c2 in encrypted_text:
        s       = pow(c1, x, p)          # s = c1^x mod p
        s_inv   = mod_inverse(s, p)       # s^-1 mod p
        m       = (c2 * s_inv) % p        # m = c2 / s mod p
        decrypted += chr(m)
    return decrypted


if __name__ == "__main__":
    
    text = input("Entrez le texte à chiffrer : ")

    # Génère les clés avec suffisamment de bits pour couvrir tous les caractères
    bits = 10
    while 2 ** bits < max(ord(c) for c in text) + 1:
        bits += 1

    public_key, private_key = elgamal_generate_keys(bits=bits)
    p, g, h = public_key
    print(f"\n  Paramètres publics  : p={p}, g={g}, h={h}")
    print(f"  Clé privée          : x={private_key[1]}")

    encrypted_text = elgamal_encrypt(text, public_key)
    print(f"\n  Texte chiffré       : {encrypted_text}")

    decrypted_text = elgamal_decrypt(encrypted_text, private_key)
    print(f"  Texte déchiffré     : {decrypted_text}")

    print("\n  ✓ Chiffrement/déchiffrement ElGamal réussi.")