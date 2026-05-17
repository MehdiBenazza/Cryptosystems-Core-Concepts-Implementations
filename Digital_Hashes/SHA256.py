

import hashlib
import struct
import os
import time

# ─── ANSI ────────────────────────────────────────────────────
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
DIM    = "\033[2m"
MAGENTA = "\033[95m"


def separator(title: str = "") -> None:
    if title:
        print(f"\n{BOLD}{CYAN}{'─'*20} {title} {'─'*20}{RESET}")
    else:
        print(f"{DIM}{'─'*60}{RESET}")



# Round constants: first 32 bits of the fractional parts of the
# cube roots of the first 64 primes
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]

# Initial hash values: first 32 bits of the fractional parts
# of the square roots of the first 8 primes
H0_INIT = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
]

MASK32 = 0xFFFFFFFF


def rotr(x: int, n: int) -> int:
    """Rotate right 32-bit integer x by n bits."""
    return ((x >> n) | (x << (32 - n))) & MASK32


def sha256_pad(message: bytes) -> bytes:
    """
    Merkle-Damgård padding:
      1. Append bit '1'  (0x80 byte)
      2. Append '0' bits until length ≡ 448 (mod 512) bits
      3. Append original length as 64-bit big-endian integer
    """
    msg_len_bits = len(message) * 8
    message += b"\x80"
    # Pad to 56 bytes mod 64
    while len(message) % 64 != 56:
        message += b"\x00"
    # Append original length (64-bit big-endian)
    message += struct.pack(">Q", msg_len_bits)
    return message


def sha256_compress(block: bytes, h: list) -> list:
    """
    Process one 512-bit block.
    Returns updated working variables [a..h].
    """
    assert len(block) == 64

    # Message schedule
    w = list(struct.unpack(">16I", block))
    for i in range(16, 64):
        s0 = rotr(w[i-15], 7) ^ rotr(w[i-15], 18) ^ (w[i-15] >> 3)
        s1 = rotr(w[i-2],  17) ^ rotr(w[i-2],  19) ^ (w[i-2] >> 10)
        w.append((w[i-16] + s0 + w[i-7] + s1) & MASK32)

    a, b, c, d, e, f, g, hh = h

    # 64 rounds of compression
    for i in range(64):
        S1  = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)
        ch  = (e & f) ^ ((~e) & g)
        temp1 = (hh + S1 + ch + K[i] + w[i]) & MASK32

        S0  = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        temp2 = (S0 + maj) & MASK32

        hh = g
        g  = f
        f  = e
        e  = (d + temp1) & MASK32
        d  = c
        c  = b
        b  = a
        a  = (temp1 + temp2) & MASK32

    return [
        (h[0] + a) & MASK32,
        (h[1] + b) & MASK32,
        (h[2] + c) & MASK32,
        (h[3] + d) & MASK32,
        (h[4] + e) & MASK32,
        (h[5] + f) & MASK32,
        (h[6] + g) & MASK32,
        (h[7] + hh) & MASK32,
    ]


def sha256_manual(data: bytes) -> str:
    """Full SHA-256 implementation. Returns hex digest."""
    padded = sha256_pad(data)
    h = list(H0_INIT)
    for i in range(0, len(padded), 64):
        h = sha256_compress(padded[i:i+64], h)
    return "".join(f"{x:08x}" for x in h)


# ──────────────────────────────────────────────────────────────
#  Part 1 : Validate against hashlib on 10 test vectors
# ──────────────────────────────────────────────────────────────

TEST_VECTORS = [
    b"",
    b"abc",
    b"hello world",
    b"The quick brown fox jumps over the lazy dog",
    b"Cryptographie Appliquee 2026",
    b"\x00",
    b"\xff" * 55,   # exactly fills one block after padding
    b"\xff" * 56,   # spills into second block
    b"a" * 1000,
    bytes(range(256)),
]


def part1_validation() -> None:
    separator("Partie 1 — Validation SHA-256 manuel vs hashlib (10 vecteurs)")

    all_ok = True
    for i, vec in enumerate(TEST_VECTORS):
        expected = hashlib.sha256(vec).hexdigest()
        got      = sha256_manual(vec)
        ok       = expected == got
        if not ok:
            all_ok = False
        label = f"Vecteur {i+1:02d} ({len(vec)} octets)"
        status = f"{GREEN}✓ OK{RESET}" if ok else f"{RED}✗ ERREUR{RESET}"
        print(f"  {status}  {YELLOW}{label:<35}{RESET}  {DIM}{got[:32]}…{RESET}")

    print()
    if all_ok:
        print(f"  {BOLD}{GREEN}✓ Toutes les 10 empreintes correspondent à hashlib.sha256(){RESET}")
    else:
        print(f"  {BOLD}{RED}✗ Certaines empreintes divergent !{RESET}")


# ──────────────────────────────────────────────────────────────
#  Part 2 : File integrity check
# ──────────────────────────────────────────────────────────────

def sha256_file(path: str) -> str:
    """Compute SHA-256 of a file in chunks (handles large files)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def part2_integrity() -> None:
    separator("Partie 2 — Vérification d'intégrité (simulation téléchargement)")

    # Simulate creating a "downloaded" archive
    archive_path = "/tmp/linux_archive_simule.bin"
    content = os.urandom(512 * 1024)          # 512 Ko of random bytes
    with open(archive_path, "wb") as f:
        f.write(content)

    # "Official" hash published on the server
    official_hash = hashlib.sha256(content).hexdigest()

    print(f"\n  {DIM}Fichier simulé     : {archive_path} ({len(content)//1024} Ko){RESET}")
    print(f"  Hash officiel (serveur) : {YELLOW}{official_hash}{RESET}")

    # ── Scenario 1 : intact file ──
    local_hash = sha256_file(archive_path)
    match = local_hash == official_hash
    print(f"\n  {BOLD}Scénario 1 — Fichier intact :{RESET}")
    print(f"  Hash local              : {GREEN}{local_hash}{RESET}")
    print(f"  Résultat : {BOLD}{GREEN}✓ OK — Intégrité vérifiée{RESET}" if match else f"  Résultat : {BOLD}{RED}✗ CORROMPU{RESET}")

    # ── Scenario 2 : corrupted file (1 byte flipped) ──
    corrupted = bytearray(content)
    corrupted[42] ^= 0xFF
    with open(archive_path, "wb") as f:
        f.write(bytes(corrupted))

    local_hash2 = sha256_file(archive_path)
    match2 = local_hash2 == official_hash
    print(f"\n  {BOLD}Scénario 2 — Fichier corrompu (1 octet modifié) :{RESET}")
    print(f"  Hash local              : {RED}{local_hash2}{RESET}")
    print(f"  Résultat : {BOLD}{RED}✗ CORROMPU — Les hashes ne correspondent pas !{RESET}" if not match2
          else f"  Résultat : {BOLD}{GREEN}✓ OK{RESET}")

    # Clean up
    os.remove(archive_path)

    print(f"\n  {DIM}→ SHA-256 détecte n'importe quelle altération, "
          f"même d'un seul bit.{RESET}")


# ─── Main ─────────────────────────────────────────────────────

def main() -> None:
    print(f"\n{BOLD}{CYAN}╔{'═'*60}╗")
    print(f"║{'TP 4 — Exercice 4.2 : SHA-256 (implémentation manuelle)':^60}║")
    print(f"╚{'═'*60}╝{RESET}")

    part1_validation()
    part2_integrity()

    print(f"\n{BOLD}{GREEN}✓ Exercice 4.2 terminé.{RESET}\n")


if __name__ == "__main__":
    main()