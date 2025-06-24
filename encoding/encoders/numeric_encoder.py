from encoding.encoders.base_encoder import BaseEncoder

class NumericEncoder(BaseEncoder):
    def __init__(self):
        super().__init__()

    def encode(self, data: str) -> str:
        def _encode_group(group: str) -> str:
            num = int(group)
            length = len(str(abs(num)))
            if length == 3:
                return format(num, '010b')
            elif length == 2:
                return format(num, '07b')
            elif length == 1:
                return format(num, '04b')
            else:
                raise ValueError("Group must be 1 to 3 digits long")
        groups = self._chunk_string(data, 3)
        return ''.join(list(map(_encode_group, groups)))