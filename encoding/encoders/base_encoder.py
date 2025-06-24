class BaseEncoder:
    def __init__(self):
        pass

    def _chunk_string(self, s: str, n: int) -> list[str]:
        return [s[i: i+n] for i in range(0, len(s), n)]

    def encode(self, data: str) -> str:
        raise NotImplementedError("Subclasses should implement this method.")