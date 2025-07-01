from copy import deepcopy
from constants.gf256_base2_primitive285 import ALPHA, LOG
from error_correction.polynomial import Polynomial

def subtract_polynomials(p1: Polynomial, p2: Polynomial) -> Polynomial:
    result_terms = {}
    for coef, exp in zip(p1.coefficients, p1.exponents):
        result_terms[exp] = result_terms.get(exp, 0) + coef
    for coef, exp in zip(p2.coefficients, p2.exponents):
        result_terms[exp] = result_terms.get(exp, 0) ^ coef
    result_items = sorted(result_terms.items(), key=lambda x: -x[0])
    result_coeffs = [coef for exp, coef in result_items if coef != 0]
    result_exps = [exp for exp, coef in result_items if coef != 0]
    if not result_coeffs:
        return Polynomial([0], [0])
    return Polynomial(result_coeffs, result_exps)    

def polynomial_division(message_polynomial: Polynomial, generator_polynomial: Polynomial) -> list:
    steps = len(message_polynomial.coefficients)
    message_polynomial.multiply_by_exp(generator_polynomial.exponents[0])
    for _ in range(steps):
        lead_term = (message_polynomial.coefficients[0], message_polynomial.exponents[0])
        product = deepcopy(generator_polynomial)
        product.multiply_by_coeff(lead_term[0])
        product.multiply_by_exp(lead_term[1] - product.exponents[0])
        message_polynomial = subtract_polynomials(message_polynomial, product)
    return message_polynomial.coefficients