from constants.qr_error_correction_codewords import EC_CODEWORDS
from error_correction.generator_polynomial import generate_generator_polynomial
from error_correction.polynomial import Polynomial
from error_correction.polynomial_division import polynomial_division

class QRReedSolomon:
    def __init__(self, data, error_correction_level, version):
        self.data = data
        self.error_correction_level = error_correction_level
        self.version = version
        ec_data = EC_CODEWORDS[(version, error_correction_level)]
        self.total_data_codewords = ec_data['Total Data Codewords']
        self.group1_blocks = ec_data['Group1']['Blocks']
        self.group1_block_size = ec_data['Group1']['Data CW/Block']
        self.group2_blocks = ec_data['Group2']['Blocks']
        self.group2_block_size = ec_data['Group2']['Data CW/Block']
        self.ec_codewords_len = ec_data['EC Codewords Per Block']
    
    def make_groups(self):
        codewords = [self.data[i: i + 8] for i in range(0, len(self.data), 8)]
        if len(codewords) != self.total_data_codewords:
            raise ValueError("Data does not match the total data codewords for the given version and error correction level.")
        group1 = codewords[:self.group1_blocks * self.group1_block_size]
        group2 = codewords[self.group1_blocks * self.group1_block_size:]
        group1 = [group1[i:i + self.group1_block_size] for i in range(0, len(group1), self.group1_block_size)]
        group2 = [group2[i:i + self.group2_block_size] for i in range(0, len(group2), max(1, self.group2_block_size))]
        group1 = [[int(b, 2) for b in block] for block in group1]
        group2 = [[int(b, 2) for b in block] for block in group2]
        self.groups = group1 + group2

    def generate_ec_codewords(self):
        self.make_groups()
        generator_polynomial = generate_generator_polynomial(self.ec_codewords_len)
        self.ec_codewords = []
        for codewords in self.groups:
            message_polynomial = Polynomial(codewords)
            block_ec_codeword = polynomial_division(
                message_polynomial,
                Polynomial(generator_polynomial.coefficients)
            )
            self.ec_codewords.append(block_ec_codeword)
        return self.ec_codewords