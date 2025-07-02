from constants.gf256_base2_primitive285 import ALPHA, LOG
from error_correction.polynomial import Polynomial

def multiply_coefficients(c1: int, c2: int) -> int:
    if c1 == 0 or c2 == 0:
        return 0
    return ALPHA[(LOG[c1] + LOG[c2]) % 255]

def multiply_polynomials(p1: Polynomial, p2: Polynomial) -> Polynomial:
    result_terms = {}
    for c1, e1 in zip(p1.coefficients, p1.exponents):
        for c2, e2 in zip(p2.coefficients, p2.exponents):
            coeff = multiply_coefficients(abs(c1), abs(c2))
            exp = e1 + e2
            result_terms[exp] = result_terms.get(exp, 0) ^ coeff
    result_terms = {e: c for e, c in result_terms.items() if c != 0}
    sorted_terms = sorted(result_terms.items(), key=lambda x: -x[0])
    if not sorted_terms:
        return Polynomial([0], [0])
    new_exponents, new_coefficients = zip(*sorted_terms)
    return Polynomial(list(new_coefficients), list(new_exponents))

def generate_generator_polynomial(n):
    generator = Polynomial([1, -1])
    for i in range(1, n):
        generator = multiply_polynomials(generator, Polynomial([1, -ALPHA[i]]))
    return generator