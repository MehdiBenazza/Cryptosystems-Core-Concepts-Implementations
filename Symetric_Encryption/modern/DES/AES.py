
import numpy as np
import secrets
from copy import deepcopy



def encode(textClear):
    byte_data = textClear.encode('utf-8')
    bits = ''.join(format(byte, '08b') for byte in byte_data)
    return bits

def generate_random_key(key_size):
    key_bytes = key_size // 8
    return secrets.token_hex(key_bytes)

def xor_matrices(a, b):
    result = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            result[i][j] = a[i][j] ^ b[i][j]
    return result

def random_matrix():
    data = secrets.token_bytes(16)
    return bytes_to_matrix(data)



def bmc(bits):
    matrices = []

    for i in range(0, len(bits), 128):
        block = bits[i:i+128]

        if len(block) < 128:
            block = block.ljust(128, '0')

        bytes_list = [block[j:j+8] for j in range(0, 128, 8)]

        matrix = [[0]*4 for _ in range(4)]

        for l in range(16):
            row = l % 4
            col = l // 4
            matrix[row][col] = int(bytes_list[l], 2)

        matrices.append(matrix)

    return matrices



def createKey(key, key_size=128):
    key = encode(key)

    if key_size == 128:
        if len(key) < 128:
            key = key.ljust(128, '0')
        else:
            key = key[:128]

        keyMatrix = [[0]*4 for _ in range(4)]
        bytes_list = [key[j:j+8] for j in range(0, 128, 8)]

        for l in range(16):
            row = l % 4
            col = l // 4
            keyMatrix[row][col] = int(bytes_list[l], 2)

        return keyMatrix

    elif key_size == 192:
        if len(key) < 192:
            key = key.ljust(192, '0')
        else:
            key = key[:192]

        keyMatrix = [[0]*6 for _ in range(4)]
        bytes_list = [key[j:j+8] for j in range(0, 192, 8)]

        for l in range(24):
            row = l % 4
            col = l // 4
            keyMatrix[row][col] = int(bytes_list[l], 2)

        return keyMatrix

    else:
        if len(key) < 256:
            key = key.ljust(256, '0')
        else:
            key = key[:256]

        keyMatrix = [[0]*8 for _ in range(4)]
        bytes_list = [key[j:j+8] for j in range(0, 256, 8)]

        for l in range(32):
            row = l % 4
            col = l // 4
            keyMatrix[row][col] = int(bytes_list[l], 2)

        return keyMatrix



S_BOX = [
    [0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76],
    [0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0],
    [0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15],
    [0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75],
    [0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84],
    [0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF],
    [0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8],
    [0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2],
    [0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73],
    [0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB],
    [0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79],
    [0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08],
    [0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A],
    [0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E],
    [0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF],
    [0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16]
]

INV_S_BOX = [[0]*16 for _ in range(16)]
for r in range(16):
    for c in range(16):
        val = S_BOX[r][c]
        INV_S_BOX[val >> 4][val & 0x0F] = (r << 4) | c

def s_box(matrix):
    s_matrix = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            val = matrix[i][j]
            row = val >> 4 & 0x0F
            col = val & 0x0F
            s_matrix[i][j] = S_BOX[row][col]
    return s_matrix

def inv_s_box(matrix):
    s_matrix = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            val = matrix[i][j]
            row = val >> 4 & 0x0F
            col = val & 0x0F
            s_matrix[i][j] = INV_S_BOX[row][col]
    return s_matrix


def shift_rows(matrix):
    for i in range(4):
        matrix[i] = np.roll(matrix[i], -i)
    return matrix

def inv_shift_rows(matrix):
    for i in range(4):
        matrix[i] = np.roll(matrix[i], i)
    return matrix



def galois_mult(a, b):
    result = 0

    for i in range(8):
        if b & 1:
            result ^= a

        carry = a & 0x80
        a <<= 1

        if carry:
            a ^= 0x11B

        a &= 0xFF
        b >>= 1

    return result

def matrix_mult(A, B):
    result = [[0]*len(B[0]) for _ in range(len(A))]

    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] ^= galois_mult(A[i][k], B[k][j])

    return result

MDS = [
    [0x02, 0x03, 0x01, 0x01],
    [0x01, 0x02, 0x03, 0x01],
    [0x01, 0x01, 0x02, 0x03],
    [0x03, 0x01, 0x01, 0x02]
]

INV_MDS = [
    [0x0E, 0x0B, 0x0D, 0x09],
    [0x09, 0x0E, 0x0B, 0x0D],
    [0x0D, 0x09, 0x0E, 0x0B],
    [0x0B, 0x0D, 0x09, 0x0E]
]

def mix_columns(matrix1, matrix2):
    return matrix_mult(matrix1, matrix2)



def key_expansion(key, key_size=128):

    Rcon = [
        [0x01,0x00,0x00,0x00],
        [0x02,0x00,0x00,0x00],
        [0x04,0x00,0x00,0x00],
        [0x08,0x00,0x00,0x00],
        [0x10,0x00,0x00,0x00],
        [0x20,0x00,0x00,0x00],
        [0x40,0x00,0x00,0x00],
        [0x80,0x00,0x00,0x00],
        [0x1B,0x00,0x00,0x00],
        [0x36,0x00,0x00,0x00]
    ]

    if key_size == 128:
        Nk = 4
        Nr = 10
    elif key_size == 192:
        Nk = 6
        Nr = 12
    else:
        Nk = 8
        Nr = 14

    total_words = 4 * (Nr + 1)

    words = [[key[j][i] for j in range(4)] for i in range(Nk)]

    rcon_index = 0

    for i in range(Nk, total_words):

        temp = words[i - 1][:]

        if i % Nk == 0:

            temp = temp[1:] + temp[:1]
            temp = [S_BOX[b >> 4][b & 0x0F] for b in temp]
            temp = [temp[j] ^ Rcon[rcon_index][j] for j in range(4)]

            rcon_index += 1

        elif Nk > 6 and i % Nk == 4:
            temp = [S_BOX[b >> 4][b & 0x0F] for b in temp]

        new_word = [words[i - Nk][j] ^ temp[j] for j in range(4)]

        words.append(new_word)

    return words

def get_round_key(words, round_num):
    round_key = [[0]*4 for _ in range(4)]

    for col in range(4):
        word = words[round_num * 4 + col]

        for row in range(4):
            round_key[row][col] = word[row]

    return round_key

def add_round_key(matrix, round_key):
    result = [[0]*4 for _ in range(4)]

    for i in range(4):
        for j in range(4):
            result[i][j] = matrix[i][j] ^ round_key[i][j]

    return result



def encrypt_block(block, words, nr):

    rk0 = get_round_key(words, 0)
    state = add_round_key(block, rk0)

    for rnd in range(1, nr):
        state = s_box(state)
        state = shift_rows(state)
        state = mix_columns(MDS, state)

        rk = get_round_key(words, rnd)
        state = add_round_key(state, rk)

    state = s_box(state)
    state = shift_rows(state)

    rk_final = get_round_key(words, nr)
    state = add_round_key(state, rk_final)

    return state

def decrypt_block(block, words, nr):

    rk_final = get_round_key(words, nr)
    state = add_round_key(block, rk_final)

    for rnd in range(nr - 1, 0, -1):

        state = inv_shift_rows(state)
        state = inv_s_box(state)

        rk = get_round_key(words, rnd)
        state = add_round_key(state, rk)

        state = mix_columns(INV_MDS, state)

    state = inv_shift_rows(state)
    state = inv_s_box(state)

    rk0 = get_round_key(words, 0)
    state = add_round_key(state, rk0)

    return state


def matrix_to_bytes(matrix):
    result = []

    for col in range(4):
        for row in range(4):
            result.append(matrix[row][col])

    return bytes(result)

def bytes_to_matrix(data):
    matrix = [[0]*4 for _ in range(4)]

    for col in range(4):
        for row in range(4):
            matrix[row][col] = data[col * 4 + row]

    return matrix

def remove_padding(data):
    return data.rstrip(b'\x00')




def ecb_encrypt(blocks, words, nr):
    encrypted = []

    for block in blocks:
        encrypted.append(encrypt_block(block, words, nr))

    return encrypted

def ecb_decrypt(blocks, words, nr):
    decrypted = []

    for block in blocks:
        decrypted.append(decrypt_block(block, words, nr))

    return decrypted

def cbc_encrypt(blocks, words, nr, iv):

    encrypted = []
    previous = deepcopy(iv)

    for block in blocks:

        xored = xor_matrices(block, previous)
        cipher = encrypt_block(xored, words, nr)

        encrypted.append(cipher)
        previous = cipher

    return encrypted

def cbc_decrypt(blocks, words, nr, iv):

    decrypted = []
    previous = deepcopy(iv)

    for block in blocks:

        decrypted_block = decrypt_block(block, words, nr)
        plain = xor_matrices(decrypted_block, previous)

        decrypted.append(plain)
        previous = block

    return decrypted

def increment_counter(counter_matrix):

    counter_bytes = bytearray(matrix_to_bytes(counter_matrix))

    for i in range(15, -1, -1):
        counter_bytes[i] = (counter_bytes[i] + 1) % 256

        if counter_bytes[i] != 0:
            break

    return bytes_to_matrix(bytes(counter_bytes))

def ctr_encrypt(blocks, words, nr, nonce):

    encrypted = []
    counter = deepcopy(nonce)

    for block in blocks:

        keystream = encrypt_block(counter, words, nr)
        cipher = xor_matrices(block, keystream)

        encrypted.append(cipher)

        counter = increment_counter(counter)

    return encrypted

ctr_decrypt = ctr_encrypt



def matrices_to_bin_string(matrices):
    result = []

    for mat in matrices:
        block_bytes = matrix_to_bytes(mat)
        bits = ''.join(format(b, '08b') for b in block_bytes)
        result.append(bits)

    return '\n'.join(result)


def matrices_to_binary_string(matrices):
    """Converts a list of state matrices into a single string of bits."""
    binary_str = ""
    for mat in matrices:
        block_bytes = matrix_to_bytes(mat)
        binary_str += ''.join(format(b, '08b') for b in block_bytes)
    return binary_str

if __name__ == "__main__":
    print("=" * 60)
    print(" AES CRYPTOSYSTEM (128/192/256 - ECB/CBC/CTR) ")
    print("=" * 60)

    print("1. Encrypt")
    print("2. Decrypt")
    action = input("Choose action (1/2): ")

    # Standard AES Parameters Setup
    print("\nAES Configuration:")
    print("1. AES-128 | 2. AES-192 | 3. AES-256")
    size_choice = input("Choose AES size: ")
    
    if size_choice == "1":
        key_size, nr = 128, 10
    elif size_choice == "2":
        key_size, nr = 192, 12
    else:
        key_size, nr = 256, 14

    print("\nMode of Operation:")
    print("1. ECB | 2. CBC | 3. CTR")
    mode = input("Choose mode: ")

    if action == "1":
        plaintext = input("\nEnter message to encrypt: ")
        
        # Key Management
        key_hex = generate_random_key(key_size)
        print(f"\n[!] SAVE THIS KEY: {key_hex}")
        
        key_matrix = createKey(key_hex, key_size)
        words = key_expansion(key_matrix, key_size)

        bits = encode(plaintext)
        blocks = bmc(bits)

        if mode == "1":
            encrypted_matrices = ecb_encrypt(blocks, words, nr)
        elif mode == "2":
            iv = random_matrix()
            print(f"[!] SAVE THIS IV (hex): {matrix_to_bytes(iv).hex()}")
            encrypted_matrices = cbc_encrypt(blocks, words, nr, iv)
        else:
            nonce = random_matrix()
            print(f"[!] SAVE THIS NONCE (hex): {matrix_to_bytes(nonce).hex()}")
            encrypted_matrices = ctr_encrypt(blocks, words, nr, nonce)

        # Output result as 1s and 0s
        print("\nENCRYPTED MESSAGE (BINARY):")
        print(matrices_to_binary_string(encrypted_matrices))

    elif action == "2":
        binary_input = input("\nEnter the binary cipher text (1s and 0s): ").strip()
        key_hex = input("Enter the Key (hex): ").strip()

        key_matrix = createKey(key_hex, key_size)
        words = key_expansion(key_matrix, key_size)

        # Convert binary string back to matrices
        matrices = []
        for i in range(0, len(binary_input), 128):
            block_bits = binary_input[i:i+128]
            if len(block_bits) < 128: break # Safety check
            block_bytes = bytes(int(block_bits[j:j+8], 2) for j in range(0, 128, 8))
            matrices.append(bytes_to_matrix(block_bytes))

        if mode == "1":
            decrypted_matrices = ecb_decrypt(matrices, words, nr)
        elif mode == "2":
            iv_hex = input("Enter the IV (hex): ")
            iv = bytes_to_matrix(bytes.fromhex(iv_hex))
            decrypted_matrices = cbc_decrypt(matrices, words, nr, iv)
        else:
            nonce_hex = input("Enter the Nonce (hex): ")
            nonce = bytes_to_matrix(bytes.fromhex(nonce_hex))
            decrypted_matrices = ctr_decrypt(matrices, words, nr, nonce)

        # Combine and decode
        full_bytes = b''.join(matrix_to_bytes(m) for m in decrypted_matrices)
        result = remove_padding(full_bytes)

        print("\nDECRYPTED MESSAGE:")
        print(result.decode('utf-8', errors='replace'))

    else:
        print("Invalid action selected.")