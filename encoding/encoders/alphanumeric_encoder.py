from encoding.encoders.base_encoder import BaseEncoder
from constants.qr_alphanumeric_values import ALPHANUMERIC_VALUES

class AlphanumericEncoder(BaseEncoder):
    def __init__(self):
        super().__init__()

    def encode(self, data: str) -> str:
        def _encode_pair(pair: str) -> str:
            if len(pair) == 2:
                return format(ALPHANUMERIC_VALUES.get(pair[0], ' ') * 45 + ALPHANUMERIC_VALUES.get(pair[1], ' '), '011b')
            elif len(pair) == 1:
                return format(ALPHANUMERIC_VALUES.get(pair[0], ' '), '06b')
            else:
                raise ValueError("Pair must be 1 or 2 characters long")
        pairs = self._chunk_string(data, 2)
        return ''.join(list(map(_encode_pair, pairs)))