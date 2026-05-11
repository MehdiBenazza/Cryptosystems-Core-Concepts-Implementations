"""
Signature numérique El-Gamal - Implémentation pédagogique
Algorithme : Signature basée sur le logarithme discret
"""

import hashlib
import random

# Alphabet pédagogique pour l'encodage des messages
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', ' ']


def pgcd(a, b):
    """Calcule le PGCD de deux nombres"""
    while b:
        a, b = b, a % b
    return a


def encoder_message(message):
    """
    Encode un message en utilisant l'alphabet pédagogique
    
    Args:
        message : message à encoder (string)
    
    Returns:
        Liste d'entiers représentant les indices des caractères dans l'alphabet
    
    Raises:
        ValueError si un caractère n'existe pas dans l'alphabet
    """
    message_lower = message.lower()
    indices = []
    for char in message_lower:
        if char not in alphabet:
            raise ValueError(f"Caractère '{char}' non trouvé dans l'alphabet")
        indices.append(alphabet.index(char))
    return indices


def est_premier(n):
    """Vérifie si n est premier"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def modularinverse(a, m):
    """Calcule l'inverse modulaire avec Euclide étendu"""
    
    def euclide_etendu(a, b):
        if a == 0:
            return b, 0, 1
        
        pgcd, x1, y1 = euclide_etendu(b % a, a)
        
        x = y1 - (b // a) * x1
        y = x1
        
        return pgcd, x, y

    pgcd_val, x, y = euclide_etendu(a, m)

    if pgcd_val != 1:
        return None

    return x % m

def trouver_generateur(p):
    """
    Trouve un générateur g du groupe multiplicatif modulo p
    Pour une implémentation pédagogique, utilise une méthode simple
    """
    # Pour p premier, g est un générateur si g^((p-1)/q) ≠ 1 mod p
    # Pour simplifier : on teste les petites valeurs
    for g in range(2, p):
        if pow(g, (p - 1) // 2, p) != 1 and pow(g, 2, p) != 1:
            return g
    return 2


def generer_cles_elgamal(p, g):
    """
    Génère une paire de clés El-Gamal
    
    Args:
        p : nombre premier
        g : générateur du groupe multiplicatif modulo p
    
    Returns:
        (cle_publique, cle_privee) : ((p, g, y), (p, g, x))
    """
    # x : clé privée (1 < x < p-1)
    x = random.randint(2, p - 2)
    
    # y = g^x mod p : clé publique
    y = pow(g, x, p)
    
    return (p, g, y), (p, g, x)


def hash_message(message):
    """
    Hash le message avec SHA-256
    
    Returns:
        Hash du message en tant qu'entier
    """
    hash_obj = hashlib.sha256(message.encode())
    hash_hex = hash_obj.hexdigest()
    # Prendre les premiers octets pour rester petit
    hash_int = int(hash_hex[:8], 16)
    return hash_int


def signer_elgamal(message, cle_privee):
    """
    Signe un message avec la clé privée El-Gamal
    
    Signature :
        r = g^k mod p
        s = (H(m) - x*r) * k^(-1) mod (p-1)
    
    Args:
        message : message à signer (string)
        cle_privee : (p, g, x)
    
    Returns:
        (r, s) : signature
    """
    p, g, x = cle_privee
    h = hash_message(message) % (p - 1)
    
    # Choisir k aléatoire (1 < k < p-1) et coprime avec (p-1)
    while True:
        k = random.randint(2, p - 2)
        if pgcd(k, p - 1) == 1:
            break
    
    # r = g^k mod p
    r = pow(g, k, p)
    
    # k_inv = k^(-1) mod (p-1)
    k_inv = modularinverse(k, p - 1)
    
    # s = (H(m) - x*r) * k_inv mod (p-1)
    s = ((h - x * r) * k_inv) % (p - 1)
    
    return (r, s)


def verifier_signature_elgamal(message, signature, cle_publique):
    """
    Vérifie une signature El-Gamal
    
    Vérification :
        u = y^r * r^s mod p
        v = g^H(m) mod p
        Valide si u == v
    
    Args:
        message : message signé
        signature : (r, s)
        cle_publique : (p, g, y)
    
    Returns:
        True si signature valide, False sinon
    """
    p, g, y = cle_publique
    r, s = signature
    h = hash_message(message) % (p - 1)
    
    # Vérifier que r et s sont dans les bonnes plages
    if r <= 0 or r >= p or s <= 0 or s >= p - 1:
        return False
    
    # u = y^r * r^s mod p
    u = (pow(y, r, p) * pow(r, s, p)) % p
    
    # v = g^H(m) mod p
    v = pow(g, h, p)
    
    return u == v


# ============ EXEMPLE D'EXÉCUTION ============

if __name__ == "__main__":
    print("=" * 60)
    print("SIGNATURE EL-GAMAL - EXEMPLE PÉDAGOGIQUE")
    print("=" * 60)
    
    # Paramètres : p premier, g générateur
    p = 23  # nombre premier petit
    g = trouver_generateur(p)
    
    print(f"\n1. Paramètres du système")
    print(f"   p = {p} (nombre premier)")
    print(f"   g = {g} (générateur modulo p)")
    
    # Générer les clés
    cle_publique, cle_privee = generer_cles_elgamal(p, g)
    p_pub, g_pub, y = cle_publique
    p_priv, g_priv, x = cle_privee
    
    print(f"\n2. Génération des clés")
    print(f"   x (clé privée) = {x}")
    print(f"   y = g^x mod p = {y}")
    print(f"   Clé publique : (p={p_pub}, g={g_pub}, y={y})")
    print(f"   Clé privée : (p={p_priv}, g={g_priv}, x={x})")
    
    # Message à signer
    message = "Alice"
    print(f"\n3. Message à signer : '{message}'")
    message_encoded = encoder_message(message)
    print(f"   Message encodé : {message_encoded}")
    h = hash_message(message) % (p - 1)
    print(f"   H(message) mod (p-1) = {h}")
    
    # Signer le message
    signature = signer_elgamal(message, cle_privee)
    r, s = signature
    print(f"\n4. Signature générée")
    print(f"   r = {r}, s = {s}")
    
    # Vérifier la signature
    est_valide = verifier_signature_elgamal(message, signature, cle_publique)
    print(f"\n5. Vérification")
    print(f"   u = y^r * r^s mod p = {(pow(y, r, p) * pow(r, s, p)) % p}")
    print(f"   v = g^(H(m) mod (p-1)) mod p = {pow(g, h, p)}")
    print(f"\n   ✓ SIGNATURE VALIDE" if est_valide else "\n   ✗ SIGNATURE INVALIDE")
    
    # Test avec un message modifié
    print(f"\n6. Test avec message modifié : '{message}' → 'Bob'")
    est_valide_modifie = verifier_signature_elgamal("Bob", signature, cle_publique)
    print(f"   ✓ SIGNATURE VALIDE" if est_valide_modifie else "   ✗ SIGNATURE INVALIDE (attendu)")
    print("\n" + "=" * 60)
