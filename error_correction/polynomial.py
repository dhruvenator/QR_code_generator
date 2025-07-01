from constants.gf256_base2_primitive285 import ALPHA, LOG

class Polynomial:
    def __init__(self, coefficients: list[int], exponents: list[int]=None):
        self.coefficients = coefficients
        self.exponents = exponents
        if not self.exponents:
            self.exponents = list(range(len(coefficients) - 1, -1, -1))
    
    def __repr__(self):
        return " + ".join(
            f"{c}x^{e}" if e != 0 else f"{c}"
            for c, e in zip(self.coefficients, self.exponents)
            if c != 0
        ) or "0"
    
    def multiply_by_coeff(self, coeff: int):
        assert coeff > 0 and coeff < 256, "Invalid scalar value"
        self.coefficients = [
            ALPHA[(LOG[c] + LOG[coeff]) % 255]
            for c in self.coefficients
        ]

    def multiply_by_exp(self, exp: int):
        self.exponents = [e + exp for e in self.exponents]