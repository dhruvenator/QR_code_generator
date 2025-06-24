from constants.qr_alphanumeric_values import ALPHANUMERIC_VALUES

# Modes supported by this QR code generator
QR_MODES = {
    'NUM': 'Numeric',
    'ALP': 'Alphanumeric',
    'BYT': 'Byte',
    'KAN': 'Kanji',
}

MODE_INDICATOR = {
    'NUM': '0001',
    'ALP': '0010',
    'BYT': '0100',
    'KAN': '1000',
}

# Alphanumeric character set (as per QR code spec)
ALPHANUMERIC_CHARACTERS = set(ALPHANUMERIC_VALUES.keys())

# Kanji detection helper using Shift JIS double-byte character ranges
def is_kanji(char):
    try:
        encoded = char.encode("shift_jis")
        return (
            len(encoded) == 2 and
            (0x81 <= encoded[0] <= 0x9F or 0xE0 <= encoded[0] <= 0xEB)
        )
    except UnicodeEncodeError:
        return False

def detect_qr_mode(s):
    if all(c in "0123456789" for c in s):
        return 'NUM', MODE_INDICATOR['NUM']
    if all(c in ALPHANUMERIC_CHARACTERS for c in s):
        return 'ALP', MODE_INDICATOR['ALP']
    if all(is_kanji(c) for c in s):
        return 'KAN', MODE_INDICATOR['KAN']
    try:
        s.encode("iso-8859-1")
        return 'BYT', MODE_INDICATOR['BYT']
    except:
        return None, None