alphabet = list("abcdefghiklmnopqrstuvwxyz")

def generate_matrix(key):
    key = key.lower().replace('j', 'i')

    seen = set()
    sequence = []

    for char in key:
        if char in alphabet and char not in seen:
            seen.add(char)
            sequence.append(char)

    for char in alphabet:
        if char not in seen:
            sequence.append(char)

    matrix = []
    for i in range(5):
        matrix.append(sequence[i*5:(i+1)*5])

    return matrix

def find_position(matrix, char):
    if char == 'j':
        char = 'i'
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j

def prepare_text(text):                    # rajouter des 'x' entre lettres indentiques
    text = text.lower().replace('j', 'i')
    result = ""
    i = 0

    while i < len(text):
        a = text[i]

        if i + 1 < len(text):
            b = text[i+1]
            if a == b:
                result += a + 'x'
                i += 1
            else:
                result += a + b
                i += 2
        else:
            result += a + 'x'
            i += 1

    return result

def playfair_encryption(text, key):
    matrix = generate_matrix(key)
    text = prepare_text(text)

    result = ""
    i = 0

    while i < len(text):
        a, b = find_position(matrix, text[i])
        c, d = find_position(matrix, text[i + 1])

        if a == c:
            result += matrix[a][(b + 1) % 5]
            result += matrix[c][(d + 1) % 5]

        elif b == d:
            result += matrix[(a + 1) % 5][b]
            result += matrix[(c + 1) % 5][d]

        else:
            result += matrix[a][d]
            result += matrix[c][b]

        i += 2

    return result

def playfair_decryption(text, key):
    matrix = generate_matrix(key)

    result = ""
    i = 0

    while i < len(text):
        a, b = find_position(matrix, text[i])
        c, d = find_position(matrix, text[i + 1])

        if a == c:
            result += matrix[a][(b - 1) % 5]
            result += matrix[c][(d - 1) % 5]

        elif b == d:
            result += matrix[(a - 1) % 5][b]
            result += matrix[(c - 1) % 5][d]

        else:
            result += matrix[a][d]
            result += matrix[c][b]

        i += 2

    return result

def main():
    while True:
        print("===== Playfair =====")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            text = input("Enter the plaintext: ")
            key = input("Enter the key: ")
            encrypted_text = playfair_encryption(text, key)
            print(f"Encrypted text: {encrypted_text}")
        
        elif choice == 2:
            text = input("Enter the ciphertext: ")
            key = input("Enter the key: ")
            decrypted_text = playfair_decryption(text, key)
            print(f"Decrypted text: {decrypted_text}")
        
        else:
            break