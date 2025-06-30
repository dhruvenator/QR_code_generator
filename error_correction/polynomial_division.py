from constants.gf256_base2_primitive285 import LOG, ANTILOG

def multiply_generator(term, generator):
    return generator

def subtract_polynomials(p1, p2):
    return [a ^ b for a, b in zip(p1, p2)]

def polynomial_division(message, generator_polynomial):
    steps = len(message)
    for _ in range(steps):
        lead_term = message[0]
        gernerator = multiply_generator(lead_term, generator_polynomial)
        message = subtract_polynomials(message, gernerator)
    return message