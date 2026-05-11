"""
Signature numérique RSA - Implémentation pédagogique
Algorithme : Génération de clés RSA, signature et vérification
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


def est_premier(n, k=5):
    """Test de primalité probabiliste (Miller-Rabin simplifié)"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Pour les petits nombres, vérification directe
    for i in range(2, int(n**0.5) + 1):
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

def generer_cles_rsa(p, q, e=65537):
    """
    Génère une paire de clés RSA
    
    Args:
        p, q : deux nombres premiers
        e : exposant public (généralement 65537, ici on peut utiliser 17)
    
    Returns:
        (clé_publique, clé_privée) : ((n, e), (n, d))
    """
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    # Vérifier que e est valide
    if pgcd(e, phi_n) != 1:
        raise ValueError("e doit être coprime avec phi(n)")
    
    # Calculer d tel que e*d ≡ 1 (mod phi(n))
    d = modularinverse(e, phi_n)
    
    return (n, e), (n, d)


def hash_message(message):
    """
    Hash le message avec SHA-256 et le réduit pour RSA
    
    Returns:
        Hash du message en tant qu'entier
    """
    hash_obj = hashlib.sha256(message.encode())
    hash_hex = hash_obj.hexdigest()
    # Prendre les 4 premiers octets pour rester petit
    hash_int = int(hash_hex[:8], 16)
    return hash_int


def signer_rsa(message, cle_privee):
    """
    Signe un message avec la clé privée RSA
    
    Args:
        message : message à signer (string)
        cle_privee : (n, d)
    
    Returns:
        signature : H(m)^d mod n
    """
    n, d = cle_privee
    h = hash_message(message) % n
    signature = pow(h, d, n)  # H(m)^d mod n
    return signature


def verifier_signature_rsa(message, signature, cle_publique):
    """
    Vérifie une signature RSA
    
    Args:
        message : message signé
        signature : valeur de signature
        cle_publique : (n, e)
    
    Returns:
        True si signature valide, False sinon
    """
    n, e = cle_publique
    h = hash_message(message) % n
    # Décrypter la signature : sig^e mod n
    h_dechiffre = pow(signature, e, n)
    return h_dechiffre == h


# ============ EXEMPLE D'EXÉCUTION ============

if __name__ == "__main__":
    print("=" * 60)
    print("SIGNATURE NUMÉRIQUE RSA - EXEMPLE PÉDAGOGIQUE")
    print("=" * 60)
    
    # Générer les clés avec deux petits nombres premiers
    p = 61
    q = 53
    e = 17
    
    print(f"\n1. Génération des clés")
    print(f"   p = {p}, q = {q}")
    print(f"   e = {e}")
    
    cle_publique, cle_privee = generer_cles_rsa(p, q, e)
    n, e_pub = cle_publique
    n_priv, d = cle_privee
    
    print(f"   n = p × q = {n}")
    print(f"   Clé publique : (n={n}, e={e_pub})")
    print(f"   Clé privée : (n={n_priv}, d={d})")
    
    # Message à signer
    message = "Alice"
    print(f"\n2. Message à signer: '{message}'")
    message_encoded = encoder_message(message)
    print(f"   Message encodé : {message_encoded}")
    h = hash_message(message) % n
    print(f"   H(message) mod n = {h}")
    
    # Signer le message
    signature = signer_rsa(message, cle_privee)
    print(f"\n3. Signature générée")
    print(f"   sig = H(m)^d mod n = {signature}")
    
    # Vérifier la signature avec la clé publique
    est_valide = verifier_signature_rsa(message, signature, cle_publique)
    print(f"\n4. Vérification de la signature")
    print(f"   sig^e mod n = {pow(signature, e_pub, n)}")
    print(f"   H(m) mod n = {h}")
    print(f"\n   ✓ SIGNATURE VALIDE" if est_valide else "\n   ✗ SIGNATURE INVALIDE")
    
    # Test avec un message modifié
    print(f"\n5. Test avec message modifié : '{message}' → 'Bob'")
    est_valide_modifie = verifier_signature_rsa("Bob", signature, cle_publique)
    print(f"   ✓ SIGNATURE VALIDE" if est_valide_modifie else "   ✗ SIGNATURE INVALIDE (attendu)")
    print("\n" + "=" * 60)
