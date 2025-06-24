from encoding.encoders.base_encoder import BaseEncoder

class ByteEncoder(BaseEncoder):
    def __init__(self):
        super().__init__()

    def encode(self, data: str) -> str:
        byte_data = data.encode('iso-8859-1')
        return ''.join(format(byte, '08b') for byte in byte_data)