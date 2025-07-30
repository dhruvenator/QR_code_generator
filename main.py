from numpy import full
from constants.qr_module_characters import MODULE
from data_masking.masking import MaskEvaluator
from encoding.data_encoding import DataEncoder
from error_correction.qr_reed_solomon import QRReedSolomon
from message_interleaving.interleaver import structure_message
from module_placement.placement import ModulePlacer

class QRCodeGenerator:
    def __init__(self, data: str, error_correction: str='L'):
        self.data = data
        self.error_correction = error_correction
    
    def _data_encoding(self):
        encoder = DataEncoder(self.data, self.error_correction)
        self.version = encoder.min_version
        self.encoded_data = encoder.encode_data()
    
    def _error_correction_coding(self):
        ec_handler = QRReedSolomon(self.encoded_data, self.error_correction, self.version)
        self.ec_codewords = ec_handler.generate_ec_codewords()
        self.data_groups = ec_handler.groups

    def _structure_final_message(self):
        self.qr_data = structure_message(self.data_groups, self.ec_codewords, self.version)

    def _module_placement_in_matrix(self):
        placer = ModulePlacer(self.version)
        self.non_data_modules = placer.non_data_modules
        self.qr = placer.place_data_bits(self.qr_data)

    def _data_masking(self):
        evaluator = MaskEvaluator(self.qr, self.non_data_modules, self.version, self.error_correction)
        self.qr = evaluator.get_best_mask()
    
    def _add_quiet_zone(self):
        new_size = self.qr.shape[0] + 8
        new_qr = full((new_size, new_size), MODULE['white'])
        new_qr[4:-4, 4:-4] = self.qr
        self.qr = new_qr

    def generate(self):
        self._data_encoding()
        self._error_correction_coding()
        self._structure_final_message()
        self._module_placement_in_matrix()
        self._data_masking()
        self._add_quiet_zone()
        return self.qr

def generate_qr_code(data, error_correction='L'):
        qr_generator = QRCodeGenerator(data, error_correction)
        qr = qr_generator.generate()
        for row in qr:
            print(''.join(['⬜' if v == MODULE['white'] else '⬛' if v == MODULE['black'] else '🟦' if v == MODULE['reserved'] else '🟨' for v in row]))

if __name__ == "__main__":
    generate_qr_code('dhruvanarayan.com', 'M')