


import hashlib
import os
import time


CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
DIM    = "\033[2m"


def separator(title: str = "") -> None:
    if title:
        print(f"\n{BOLD}{CYAN}{'─'*20} {title} {'─'*20}{RESET}")
    else:
        print(f"{DIM}{'─'*60}{RESET}")


def md5_hash(data: bytes) -> str:
    """Return the MD5 hex digest of data."""
    return hashlib.md5(data).hexdigest()


# ─── Part 1 : MD5 on 5 different messages ────────────────────

def part1_calcul_md5() -> None:
    separator("Partie 1 — Calcul MD5 sur 5 messages")

    messages = {
        "Chaîne vide":   b"",
        "1 octet":       b"A",
        "1 Ko":          os.urandom(1_024),
        "1 Mo":          os.urandom(1_048_576),
        "Fichier binaire (simulé)": bytes(range(256)) * 4,
    }

    for label, data in messages.items():
        digest = md5_hash(data)
        bits   = len(bytes.fromhex(digest)) * 8
        print(f"  {YELLOW}{label:<25}{RESET}  "
              f"MD5 = {GREEN}{digest}{RESET}  "
              f"({bits} bits)")

    print(f"\n  {DIM}→ Toutes les sorties font bien {BOLD}128 bits{RESET}{DIM} (32 caractères hex){RESET}")


# ─── Part 2 : Avalanche effect ───────────────────────────────

def flip_bit(data: bytes, bit_index: int) -> bytes:
    """Flip a single bit in a byte string."""
    byte_idx = bit_index // 8
    bit_in_byte = 7 - (bit_index % 8)
    lst = bytearray(data)
    lst[byte_idx] ^= (1 << bit_in_byte)
    return bytes(lst)


def bit_difference_rate(h1: str, h2: str) -> float:
    """Return the fraction of bits that differ between two hex digests."""
    b1 = int(h1, 16)
    b2 = int(h2, 16)
    xor = b1 ^ b2
    differing = bin(xor).count("1")
    total = len(h1) * 4          # 1 hex char = 4 bits
    return differing / total


def part2_avalanche() -> None:
    separator("Partie 2 — Effet Avalanche MD5")

    test_cases = [
        ("Hello, World!",     b"Hello, World!"),
        ("Cryptographie 2026", b"Cryptographie 2026"),
        ("AAAAAAAA",           b"AAAAAAAA"),
    ]

    for label, msg in test_cases:
        # Ensure at least 1 byte so we can flip bit 0
        if len(msg) == 0:
            msg = b"\x00"

        original_hash = md5_hash(msg)
        modified_msg  = flip_bit(msg, 0)          # flip 1 bit
        modified_hash = md5_hash(modified_msg)
        rate          = bit_difference_rate(original_hash, modified_hash)

        print(f"\n  Message  : {YELLOW}{label}{RESET}")
        print(f"  Original : {GREEN}{original_hash}{RESET}")
        print(f"  Modifié  : {GREEN}{modified_hash}{RESET}")

        color = GREEN if 0.40 <= rate <= 0.60 else RED
        print(f"  Bits différents : {color}{rate*100:.1f}%{RESET}  "
              f"{'✓ ≈ 50 % (bon effet avalanche)' if 0.40 <= rate <= 0.60 else '✗ Hors norme'}")

    print(f"\n  {DIM}→ Un bon hash doit changer ≈ 50 % de ses bits "
          f"quand 1 seul bit du message change.{RESET}")


# ─── Main ─────────────────────────────────────────────────────

def main() -> None:
    print(f"\n{BOLD}{CYAN}╔{'═'*56}╗")
    print(f"║{'TP 4 — Exercice 4.1 : MD5 (Message Digest 5)':^56}║")
    print(f"╚{'═'*56}╝{RESET}")

    part1_calcul_md5()
    part2_avalanche()

    print(f"\n{BOLD}{GREEN}✓ Exercice 4.1 terminé.{RESET}\n")


if __name__ == "__main__":
    main()