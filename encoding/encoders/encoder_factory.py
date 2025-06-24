from encoding.encoders.alphanumeric_encoder import AlphanumericEncoder
from encoding.encoders.base_encoder import BaseEncoder
from encoding.encoders.byte_encoder import ByteEncoder
from encoding.encoders.kanji_encoder import KanjiEncoder
from encoding.encoders.numeric_encoder import NumericEncoder

ENCODER_MODE = {
    'NUM': NumericEncoder,
    'ALP': AlphanumericEncoder,
    'BYT': ByteEncoder,
    'KAN': KanjiEncoder
}

def encoder_factory(mode: str) -> BaseEncoder:
    if mode not in ENCODER_MODE:
        raise ValueError(f"Unsupported mode: {mode}")
    return ENCODER_MODE[mode]()