import random
from math import gcd

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


def dh_generate_params(bits=10):
    """
    Génère les paramètres publics (p, g) :
      p  – grand nombre premier
      g  – racine primitive de Zp*
    """
    p = generate_large_prime(bits)
    g = find_primitive_root(p)
    return p, g


def dh_generate_private_key(p):
    """Génère une clé privée aléatoire dans ]1, p-1[."""
    return random.randint(2, p - 2)


def dh_compute_public_key(g, private_key, p):
    """Calcule la clé publique : A = g^a mod p."""
    return pow(g, private_key, p)


def dh_compute_shared_secret(public_key_other, private_key, p):
    """Calcule le secret partagé : s = B^a mod p (ou A^b mod p)."""
    return pow(public_key_other, private_key, p)


def diffie_hellman_demo():
    """
    Simule un échange Diffie-Hellman complet entre Alice et Bob,
    puis retourne le secret partagé (utilisable comme clé symétrique).
    """
    # Paramètres publics
    p, g = dh_generate_params(bits=12)

    # Clés privées
    a = dh_generate_private_key(p)   # privée Alice
    b = dh_generate_private_key(p)   # privée Bob

    # Clés publiques
    A = dh_compute_public_key(g, a, p)   # Alice envoie A à Bob
    B = dh_compute_public_key(g, b, p)   # Bob envoie B à Alice

    # Secrets partagés (doivent être égaux)
    secret_alice = dh_compute_shared_secret(B, a, p)
    secret_bob   = dh_compute_shared_secret(A, b, p)

    assert secret_alice == secret_bob, "Erreur : les secrets ne correspondent pas !"

    return {
        "p": p,
        "g": g,
        "private_key_alice": a,
        "private_key_bob": b,
        "public_key_alice": A,
        "public_key_bob": B,
        "shared_secret": secret_alice,
    }

if __name__ == "__main__":

    dh = diffie_hellman_demo()
    print(f"  Paramètres publics  : p={dh['p']}, g={dh['g']}")
    print(f"  Clé privée Alice    : {dh['private_key_alice']}")
    print(f"  Clé privée Bob      : {dh['private_key_bob']}")
    print(f"  Clé publique Alice  : {dh['public_key_alice']}")
    print(f"  Clé publique Bob    : {dh['public_key_bob']}")
    print(f"  Secret partagé      : {dh['shared_secret']}")
    print("  ✓ Les deux parties ont le même secret partagé.\n")