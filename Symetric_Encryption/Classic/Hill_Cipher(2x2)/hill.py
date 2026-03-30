from Affine import mod_inverse

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
         'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']

def inverse_matrix(matrix):
    det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det_inv = mod_inverse(det, len(alphabet))
    if det_inv == 0:
        raise ValueError("Inverse does not exist. The determinant must be coprime with the length of the alphabet.")
    return [[matrix[1][1] * det_inv % len(alphabet), -matrix[0][1] * det_inv % len(alphabet)],
            [-matrix[1][0] * det_inv % len(alphabet), matrix[0][0] * det_inv % len(alphabet)]]

def hill_encryption(text, matrix):
    if len(text) % 2 != 0:
            text += 'x'         #  On rajoute un caractère de remplissage si le texte a une longueur impaire
    result = ""
    for i in range(0, len(text), 2):
          result += alphabet[(matrix[0][0] * alphabet.index(text[i]) + matrix[0][1] * alphabet.index(text[i+1])) % len(alphabet)]
          result += alphabet[(matrix[1][0] * alphabet.index(text[i]) + matrix[1][1] * alphabet.index(text[i+1])) % len(alphabet)]
    return result

def hill_decryption(text, matrix):
    matrix_inv = inverse_matrix(matrix)
    result = ""
    if len(text) % 2 != 0:
            text += 'x'         #  On rajoute un caractère de remplissage si le texte a une longueur impaire
    for i in range(0, len(text), 2):
        result += alphabet[(matrix_inv[0][0] * alphabet.index(text[i]) + matrix_inv[0][1] * alphabet.index(text[i+1])) % len(alphabet)]
        result += alphabet[(matrix_inv[1][0] * alphabet.index(text[i]) + matrix_inv[1][1] * alphabet.index(text[i+1])) % len(alphabet)]
    return result