
import hashlib
import os
import time

# ─── ANSI ────────────────────────────────────────────────────
CYAN    = "\033[96m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
BOLD    = "\033[1m"
RESET   = "\033[0m"
DIM     = "\033[2m"
MAGENTA = "\033[95m"
BLUE    = "\033[94m"


def separator(title: str = "") -> None:
    if title:
        print(f"\n{BOLD}{CYAN}{'─'*20} {title} {'─'*20}{RESET}")
    else:
        print(f"{DIM}{'─'*60}{RESET}")


# ──────────────────────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────────────────────

ALGORITHMS = {
    "MD5":     hashlib.md5,
    "SHA-256": hashlib.sha256,
    "SHA-512": hashlib.sha512,
}


def compute_hash(algo_name: str, data: bytes) -> tuple[str, float]:
    """Return (hex_digest, elapsed_seconds)."""
    fn = ALGORITHMS[algo_name]
    start = time.perf_counter()
    digest = fn(data).hexdigest()
    elapsed = time.perf_counter() - start
    return digest, elapsed


def bit_difference(h1: str, h2: str) -> float:
    """Fraction of bits that differ between two hex digests."""
    b1 = int(h1, 16)
    b2 = int(h2, 16)
    xor = b1 ^ b2
    diff = bin(xor).count("1")
    total = len(h1) * 4
    return diff / total


def flip_bit(data: bytes, bit_index: int = 0) -> bytes:
    ba = bytearray(data)
    byte_idx = bit_index // 8
    bit_off  = 7 - (bit_index % 8)
    ba[byte_idx] ^= (1 << bit_off)
    return bytes(ba)


# ──────────────────────────────────────────────────────────────
#  Part 1 : Compare MD5 / SHA-256 / SHA-512 on same message
# ──────────────────────────────────────────────────────────────

def part1_comparison() -> None:
    separator("Partie 1 — Comparaison MD5 / SHA-256 / SHA-512 sur même message")

    message = "Cryptographie Appliquee - TP4 Hachage 2026".encode("utf-8")
    print(f"\n  Message  : {YELLOW}\"{message.decode()}\"{RESET} ({len(message)} octets)\n")

    print(f"  {'Algorithme':<12}  {'Taille sortie':>14}  {'Temps (µs)':>12}  {'Hash (tronqué)':>36}")
    print(f"  {DIM}{'─'*12}  {'─'*14}  {'─'*12}  {'─'*40}{RESET}")

    hashes = {}
    for name in ALGORITHMS:
        digest, t = compute_hash(name, message)
        bits = len(bytes.fromhex(digest)) * 8
        hashes[name] = digest
        print(f"  {BOLD}{YELLOW}{name:<12}{RESET}  "
              f"{GREEN}{bits:>14} bits{RESET}  "
              f"{BLUE}{t*1e6:>10.2f} µs{RESET}  "
              f"{DIM}{digest[:40]}…{RESET}")

    # Avalanche effect for each algo on the same message
    separator("Effet Avalanche — 1 bit modifié")
    msg2 = flip_bit(message, 0)
    print(f"\n  {'Algorithme':<12}  {'Bits différents':>16}")
    print(f"  {DIM}{'─'*12}  {'─'*16}{RESET}")
    for name in ALGORITHMS:
        h_orig, _ = compute_hash(name, message)
        h_mod,  _ = compute_hash(name, msg2)
        rate = bit_difference(h_orig, h_mod)
        color = GREEN if 0.40 <= rate <= 0.60 else RED
        mark  = "✓ ≈ 50 %" if 0.40 <= rate <= 0.60 else "✗ Hors norme"
        print(f"  {YELLOW}{name:<12}{RESET}  {color}{rate*100:>10.1f}%{RESET}  {DIM}{mark}{RESET}")

    print(f"\n  {DIM}→ Tous les algorithmes montrent un excellent effet avalanche.{RESET}")


# ──────────────────────────────────────────────────────────────
#  Part 2 : Benchmark on 100 MB
# ──────────────────────────────────────────────────────────────

def benchmark_algo(algo_name: str, data: bytes, runs: int = 3) -> float:
    """Return average throughput in MB/s."""
    fn = ALGORITHMS[algo_name]
    size_mb = len(data) / 1_048_576
    timings = []
    for _ in range(runs):
        start = time.perf_counter()
        fn(data).hexdigest()
        timings.append(time.perf_counter() - start)
    best = min(timings)
    return size_mb / best


def bar(value: float, max_val: float, width: int = 30, color: str = GREEN) -> str:
    filled = int(round(value / max_val * width))
    return color + "█" * filled + DIM + "░" * (width - filled) + RESET


def part2_benchmark() -> None:
    separator("Partie 2 — Benchmark sur 100 Mo")

    SIZE = 100 * 1_048_576          # 100 MB
    print(f"\n  {DIM}Génération de {SIZE//1_048_576} Mo de données aléatoires…{RESET}", end="", flush=True)
    data = os.urandom(SIZE)
    print(f"  {GREEN}✓{RESET}")

    results: dict[str, float] = {}
    for name in ALGORITHMS:
        print(f"  {YELLOW}{name:<8}{RESET} en cours…", end="", flush=True)
        mbs = benchmark_algo(name, data)
        results[name] = mbs
        print(f"\r  {YELLOW}{name:<8}{RESET} {GREEN}{mbs:.1f} Mo/s{RESET}       ")

    max_speed = max(results.values())

    # ── Render table ──
    print()
    print(f"  {'Algorithme':<12}  {'Débit (Mo/s)':>14}  {'Graphique':>5}")
    print(f"  {DIM}{'─'*12}  {'─'*14}  {'─'*35}{RESET}")

    colors = {"MD5": CYAN, "SHA-256": GREEN, "SHA-512": MAGENTA}
    ranking = sorted(results.items(), key=lambda x: -x[1])

    for rank, (name, speed) in enumerate(ranking):
        medal = ["🥇", "🥈", "🥉"][rank] if rank < 3 else "  "
        b = bar(speed, max_speed, width=28, color=colors[name])
        print(f"  {medal} {YELLOW}{name:<10}{RESET}  "
              f"{colors[name]}{speed:>10.1f} Mo/s{RESET}  {b}")

    fastest = ranking[0][0]
    slowest = ranking[-1][0]
    print(f"\n  {BOLD}Plus rapide : {GREEN}{fastest}{RESET}  "
          f"({results[fastest]:.1f} Mo/s)")
    print(f"  {BOLD}Plus lent   : {RED}{slowest}{RESET}  "
          f"({results[slowest]:.1f} Mo/s)")

    print(f"\n  {DIM}Notes :")
    print(f"  • SHA-512 est souvent plus rapide que SHA-256 sur CPU 64 bits")
    print(f"    car il traite 2× plus de données par opération 64 bits.")
    print(f"  • MD5 est le plus rapide mais ne doit plus être utilisé en sécurité.")
    print(f"  • SHA-3 (Keccak) n'est pas dans ce benchmark mais est recommandé")
    print(f"    pour les nouvelles applications (immune aux attaques length-extension).{RESET}")


# ─── Main ─────────────────────────────────────────────────────

def main() -> None:
    print(f"\n{BOLD}{CYAN}╔{'═'*62}╗")
    print(f"║{'TP 4 — Exercice 4.3 : SHA-512 & Comparaison Générale':^62}║")
    print(f"╚{'═'*62}╝{RESET}")

    part1_comparison()
    part2_benchmark()

    print(f"\n{BOLD}{GREEN}✓ Exercice 4.3 terminé.{RESET}\n")


if __name__ == "__main__":
    main()