from encoding.data_encoding import DataEncoder
from error_correction.qr_reed_solomon import QRReedSolomon

class QRCodeGenerator:
    def __init__(self, data, error_correction='L'):
        self.data = data
        self.error_correction = error_correction
    
    def _data_encoding(self):
        encoder = DataEncoder(self.data, self.error_correction)
        self.version = encoder.min_version
        self.encoded_data = encoder.encode_data()
    
    def _error_correction_coding(self):
        ec_handler = QRReedSolomon(self.encoded_data, self.error_correction, self.version)
        self.ec_codewords = ec_handler.generate_ec_codewords()

    def _structure_final_message(self):
        pass

    def _module_placement_in_matrix(self):
        pass

    def _data_masking(self):
        pass

    def _format_and_version_information(self):
        pass

    def generate(self):
        self._data_encoding()
        self._error_correction_coding()
        self._structure_final_message()
        self._module_placement_in_matrix()
        self._data_masking()
        self._format_and_version_information()

def generate_qr_code(data, error_correction='L'):
        qr_generator = QRCodeGenerator(data, error_correction)
        return qr_generator.generate()

if __name__ == "__main__":
    generate_qr_code('HELLO WORLD', 'Q')
    generate_qr_code('8675309')
    generate_qr_code('Hello, world!')