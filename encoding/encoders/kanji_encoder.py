from encoding.encoders.base_encoder import BaseEncoder

class KanjiEncoder(BaseEncoder):
    def __init__(self):
        super().__init__()

    def encode(self, data: str) -> str:
        return ''