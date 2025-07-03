from itertools import zip_longest
from constants.qr_remainder_bits import REMAINDER_BITS
    
def process_interleaving(groups: list[list[int]], ec_codewords: list[list[int]]) -> list:
    def interleave(collection: list):
        return [item for group in zip_longest(*collection) for item in group if item is not None]
    interleaved_data = interleave(groups)
    interleaved_ec = interleave(ec_codewords)
    return interleaved_data + interleaved_ec

def structure_message(groups: list[list[int]], ec_codewords: list[list[int]], version) -> str:
    if len(groups) == 1:
        final_message = groups[0] + ec_codewords[0]
    else:
        final_message = process_interleaving(groups, ec_codewords)
    final_message = ''.join([format(num, '08b') for num in final_message])
    final_message += '0' * REMAINDER_BITS[version]
    return final_message