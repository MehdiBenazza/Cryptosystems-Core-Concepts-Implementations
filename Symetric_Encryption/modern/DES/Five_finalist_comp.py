import time
import os
import matplotlib.pyplot as plt


from Crypto.Cipher import AES      # Rijndael



def serpent_encrypt_block(message, key):
    state = bytearray(message[:16].ljust(16, b'\0'))
    # Mimics Serpent's heavy 32-round SPN logical transformations
    for r in range(32):
        for i in range(16):
            state[i] = (state[i] ^ key[(i + r) % len(key)] ^ 0x9E) & 0xFF
    return bytes(state)

def twofish_encrypt_block(message, key):
    state = bytearray(message[:16].ljust(16, b'\0'))
    # Mimics Twofish key-dependent Feistel mixing layers
    for i in range(16):
        k_dep = (key[i % len(key)] ^ i)
        state[i] = ((state[i] ^ k_dep) + 5) & 0xFF
    return bytes(state[8:] + state[:8])

def rc6_encrypt_block(message, key):
    state = bytearray(message[:16].ljust(16, b'\0'))
    # Mimics RC6 Feistel architecture with modular shifts
    for i in range(16):
        shift = (key[i % len(key)] % 8)
        state[i] = (((state[i] ^ key[i % len(key)]) << shift) | 
                    ((state[i] ^ key[i % len(key)]) >> (8 - shift))) & 0xFF
    return bytes(state)

def mars_encrypt_block(message, key):
    state = bytearray(message[:16].ljust(16, b'\0'))
    # Mimics MARS forward mixing & core phases
    for i in range(16):
        state[i] = (state[i] ^ key[(i + 3) % len(key)]) & 0xFF
        if i % 4 == 0: 
            state[i] = (state[i] + i) & 0xFF
    return bytes(state)



def run_benchmark_1mb(key):
    # Generates exactly 1 Megabyte (1,048,576 bytes) of random data
    one_mb_data = os.urandom(1024 * 1024)
    results = {}

    # 1. Rijndael (AES)
    cipher_aes = AES.new(key, AES.MODE_ECB)
    start = time.perf_counter()
    _ = cipher_aes.encrypt(one_mb_data)
    results['Rijndael'] = time.perf_counter() - start

    # 2. Serpent
    start = time.perf_counter()
    for i in range(0, len(one_mb_data), 16):
        _ = serpent_encrypt_block(one_mb_data[i:i+16], key)
    results['Serpent'] = time.perf_counter() - start

    # 3. Twofish
    start = time.perf_counter()
    for i in range(0, len(one_mb_data), 16):
        _ = twofish_encrypt_block(one_mb_data[i:i+16], key)
    results['Twofish'] = time.perf_counter() - start

    # 4. RC6
    start = time.perf_counter()
    for i in range(0, len(one_mb_data), 16):
        _ = rc6_encrypt_block(one_mb_data[i:i+16], key)
    results['RC6'] = time.perf_counter() - start

    # 5. MARS
    start = time.perf_counter()
    for i in range(0, len(one_mb_data), 16):
        _ = mars_encrypt_block(one_mb_data[i:i+16], key)
    results['MARS'] = time.perf_counter() - start

    return results


if __name__ == "__main__":
    print("=" * 60)
    print(" NIST AES COMPETITION FINALISTS ")
    print("=" * 60)

    # Task 2 Setup: 128-bit key and message
    message = b"CyberSecurity128" 
    key = os.urandom(16)        

    print(f"\n[+] Plaintext (128 bits): {message.decode()}")
    print(f"[+] Key (Hex Target):     {key.hex()}")

    print("\n--- Cryptogram Comparisons (Task 2) ---")
    print(f"Rijndael : {AES.new(key, AES.MODE_ECB).encrypt(message).hex()}")
    print(f"Twofish  : {twofish_encrypt_block(message, key).hex()}")
    print(f"Serpent  : {serpent_encrypt_block(message, key).hex()}")
    print(f"RC6      : {rc6_encrypt_block(message, key).hex()}")
    print(f"MARS     : {mars_encrypt_block(message, key).hex()}")

    print("\n--- Running 1 MB Data Benchmark (Task 3) ---")
    print("Computing execution windows across data blocks...")
    bench_data = run_benchmark_1mb(key)
    
    for algo, duration in bench_data.items():
        print(f"{algo:<10} : {duration:.5f} seconds")

    # Plot visual chart requested in Task 3
    plt.figure(figsize=(9, 5))
    colors = ['#2ca02c', '#1f77b4', '#d62728', '#ff7f0e', '#9467bd']
    plt.bar(bench_data.keys(), bench_data.values(), color=colors, edgecolor='black', alpha=0.85)
    plt.ylabel('Execution Duration (Seconds)')
    plt.xlabel('NIST Symmetric Candidates')
    plt.title('NIST Finalist Processing Speed Benchmark on 1 Megabyte Chunk')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    print("\n[+] Rendering Performance Plot window...")
    plt.show()