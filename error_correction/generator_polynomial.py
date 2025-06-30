from constants.gf256_base2_primitive285 import LOG, ANTILOG

def gf_mul(x, y):
    """Multiply two numbers in GF(256)"""
    if x == 0 or y == 0:
        return 0
    return LOG[(ANTILOG[x] + ANTILOG[y]) % 255]

def poly_mul(p1, p2):
    """Multiply two polynomials in GF(256)"""
    result = [0] * (len(p1) + len(p2) - 1)
    for i in range(len(p1)):
        for j in range(len(p2)):
            result[i + j] ^= gf_mul(p1[i], p2[j])
    return result

def generate_generator_polynomial(n):
    """Generate the generator polynomial of degree n"""
    g = [1]
    for i in range(n):
        g = poly_mul(g, [1, LOG[i]])
    return [ANTILOG[coeff] for coeff in g]
