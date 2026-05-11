"""
Signature numérique DSA (Digital Signature Algorithm) - Implémentation pédagogique
Algorithme : Variante El-Gamal avec ordre d'un sous-groupe
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

def generer_parametres_dsa(p, q):
    """
    Génère les paramètres DSA
    
    Args:
        p : grand nombre premier tel que q divise (p-1)
        q : petit nombre premier divisant (p-1)
    
    Returns:
        (p, q, g) : paramètres système
    """
    # Trouver g tel que g^q ≡ 1 (mod p) et g ≠ 1
    # Pour simplifier : on trouve un générateur du sous-groupe d'ordre q
    h = 2
    while True:
        g = pow(h, (p - 1) // q, p)
        if g > 1:
            break
        h += 1
    
    return p, q, g


def generer_cles_dsa(p, q, g):
    """
    Génère une paire de clés DSA
    
    Args:
        p, q, g : paramètres du système
    
    Returns:
        (cle_publique, cle_privee) : ((p, q, g, y), (p, q, g, x))
    """
    # x : clé privée (0 < x < q)
    x = random.randint(1, q - 1)
    
    # y = g^x mod p : clé publique
    y = pow(g, x, p)
    
    return (p, q, g, y), (p, q, g, x)


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


def signer_dsa(message, cle_privee):
    """
    Signe un message avec la clé privée DSA
    
    Signature :
        Choisir k aléatoire (0 < k < q)
        r = (g^k mod p) mod q
        s = k^(-1) * (H(m) + x*r) mod q
    
    Args:
        message : message à signer (string)
        cle_privee : (p, q, g, x)
    
    Returns:
        (r, s) : signature
    """
    p, q, g, x = cle_privee
    h = hash_message(message) % q
    
    # Signer avec k aléatoire jusqu'à r ≠ 0 et s ≠ 0
    while True:
        k = random.randint(1, q - 1)
        
        # r = (g^k mod p) mod q
        r = pow(g, k, p) % q
        
        if r == 0:
            continue
        
        # k_inv = k^(-1) mod q
        k_inv = modularinverse(k, q)
        
        # s = k_inv * (H(m) + x*r) mod q
        s = (k_inv * (h + x * r)) % q
        
        if s != 0:
            break
    
    return (r, s)


def verifier_signature_dsa(message, signature, cle_publique):
    """
    Vérifie une signature DSA
    
    Vérification :
        w = s^(-1) mod q
        u1 = (H(m) * w) mod q
        u2 = (r * w) mod q
        v = ((g^u1 * y^u2) mod p) mod q
        Valide si v == r
    
    Args:
        message : message signé
        signature : (r, s)
        cle_publique : (p, q, g, y)
    
    Returns:
        True si signature valide, False sinon
    """
    p, q, g, y = cle_publique
    r, s = signature
    h = hash_message(message) % q
    
    # Vérifier que r et s sont dans les bonnes plages
    if r <= 0 or r >= q or s <= 0 or s >= q:
        return False
    
    # w = s^(-1) mod q
    w = modularinverse(s, q)
    if w is None:
        return False
    
    # u1 = (H(m) * w) mod q
    u1 = (h * w) % q
    
    # u2 = (r * w) mod q
    u2 = (r * w) % q
    
    # v = ((g^u1 * y^u2) mod p) mod q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
    
    return v == r


# ============ EXEMPLE D'EXÉCUTION ============

if __name__ == "__main__":
    print("=" * 60)
    print("SIGNATURE DSA - EXEMPLE PÉDAGOGIQUE")
    print("=" * 60)
    
    # Paramètres DSA pédagogiques
    # p et q doivent satisfaire : q | (p-1)
    q = 11  # petit nombre premier
    p = 23  # petit nombre premier, q divise (p-1) : 23-1=22, et 11|22 ✓
    
    print(f"\n1. Paramètres du système")
    print(f"   p = {p} (nombre premier)")
    print(f"   q = {q} (nombre premier divisant p-1)")
    print(f"   Vérification : (p-1) mod q = {(p-1) % q}")
    
    # Générer g et les clés
    p, q, g = generer_parametres_dsa(p, q)
    print(f"   g = {g} (générateur du sous-groupe d'ordre q)")
    
    cle_publique, cle_privee = generer_cles_dsa(p, q, g)
    p_pub, q_pub, g_pub, y = cle_publique
    p_priv, q_priv, g_priv, x = cle_privee
    
    print(f"\n2. Génération des clés")
    print(f"   x (clé privée) = {x}")
    print(f"   y = g^x mod p = {y}")
    print(f"   Clé publique : (p={p_pub}, q={q_pub}, g={g_pub}, y={y})")
    print(f"   Clé privée : (p={p_priv}, q={q_priv}, g={g_priv}, x={x})")
    
    # Message à signer
    message = "Alice"
    print(f"\n3. Message à signer : '{message}'")
    message_encoded = encoder_message(message)
    print(f"   Message encodé : {message_encoded}")
    h = hash_message(message) % q
    print(f"   H(message) mod q = {h}")
    
    # Signer le message
    signature = signer_dsa(message, cle_privee)
    r, s = signature
    print(f"\n4. Signature générée")
    print(f"   r = {r}, s = {s}")
    
    # Vérifier la signature
    est_valide = verifier_signature_dsa(message, signature, cle_publique)
    
    print(f"\n5. Vérification")
    w = modularinverse(s, q)
    u1 = (h * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
    print(f"   w = s^(-1) mod q = {w}")
    print(f"   u1 = (H(m) mod q * w) mod q = {u1}")
    print(f"   u2 = (r * w) mod q = {u2}")
    print(f"   v = ((g^u1 * y^u2) mod p) mod q = {v}")
    print(f"   r = {r}")
    print(f"\n   ✓ SIGNATURE VALIDE" if est_valide else "\n   ✗ SIGNATURE INVALIDE")
    
    # Test avec un message modifié
    print(f"\n6. Test avec message modifié : '{message}' → 'Bob'")
    est_valide_modifie = verifier_signature_dsa("Bob", signature, cle_publique)
    print(f"   ✓ SIGNATURE VALIDE" if est_valide_modifie else "   ✗ SIGNATURE INVALIDE (attendu)")
    print("\n" + "=" * 60)
