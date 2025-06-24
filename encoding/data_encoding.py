from constants.qr_character_count_bits import QR_CHARACTER_COUNT_BITS
from constants.qr_error_correction_codewords import EC_CODEWORDS
from constants.qr_version_data import CHARACTER_CAPACITIES
from encoding.mode_analysis import detect_qr_mode
from encoding.encoders.encoder_factory import encoder_factory

ERROR_CORRECTION_LEVEL = {
    'L': 7,
    'M': 15,
    'Q': 25,
    'H': 30
}

class DataEncoder:
    def __init__(self, raw_data, error_correction='L'):
        self.raw_data = raw_data
        self.error_correction = error_correction if error_correction in ERROR_CORRECTION_LEVEL else 'L'
        self.mode, self.mode_indicator = detect_qr_mode(raw_data)
        self.encoder = encoder_factory(self.mode)
        self._get_min_version()
        self._get_character_count_bits()
        self.num_bits = EC_CODEWORDS[(self.min_version, self.error_correction)]['Total Data Codewords'] * 8
    
    def _get_min_version(self):
        versions = sorted(CHARACTER_CAPACITIES.keys())
        for version in versions:
            capacities = CHARACTER_CAPACITIES[version][self.error_correction]
            if self.mode in capacities and len(self.raw_data) <= capacities[self.mode]:
                self.min_version = version
                return
        self.min_version = max(versions)
        self.raw_data = self.raw_data[:CHARACTER_CAPACITIES[self.min_version][self.error_correction][self.mode]]

    def _get_character_count_bits(self):
        num_bits = 0
        for version_range, bits in QR_CHARACTER_COUNT_BITS.items():
            if self.min_version in range(version_range[0], version_range[1] + 1):
                num_bits = bits[self.mode]
                break
        count = bin(len(self.raw_data))[2:]
        self.count_indicator = '0' * (num_bits - len(count)) + count
    
    def _add_terminator(self):
        self.terminator = ('0' * (self.num_bits - len(self.data)))[:4]
        self.data += self.terminator

    def _pad_to_make_multiple_of_8(self):
        if len(self.data) % 8 == 0:
            return
        next_multiple_of_8 = (len(self.data) // 8 + 1) * 8
        padding_length = next_multiple_of_8 - len(self.data)
        self.data += '0' * padding_length

    def _add_pad_bytes(self):
        pad_bytes = ['11101100', '00010001']
        pad_index = 0
        while len(self.data) + 8 <= self.num_bits:
            self.data += pad_bytes[pad_index]
            pad_index = 1 - pad_index
    
    def encode_data(self):
        encoded_data = self.encoder.encode(self.raw_data)
        self.data = self.mode_indicator + self.count_indicator + encoded_data
        self._add_terminator()
        self._pad_to_make_multiple_of_8()
        self._add_pad_bytes()
        return self.data