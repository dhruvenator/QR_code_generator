from numpy import ndarray, array
from constants.qr_format_strings import FORMAT_STRINGS
from constants.qr_module_characters import QR_BIT
from constants.qr_version_strings import VERSION_STRINGS

def add_version_information(qr: ndarray, version: int) -> ndarray:
    version_info = VERSION_STRINGS.get(version, '')
    if not version_info:
        raise ValueError(f'Invalid QR version: {version}')
    size = qr.shape[0]
    version_bits = array([QR_BIT[int(bit)] for bit in version_info][::-1])
    assert len(version_bits) == 18, 'Version information must be 18 bits long'
    version_bits = version_bits.reshape(6,3)
    qr[:6, size-11:size-8] = version_bits
    qr[size-11:size-8, :6] = version_bits.T
    return qr

def add_format_information(qr: ndarray, error_correction: str, mask_pattern: int) -> ndarray:
    format_info = FORMAT_STRINGS[(error_correction, mask_pattern)]
    format_bits = array([QR_BIT[int(bit)] for bit in format_info])
    assert len(format_bits) == 15, 'Format information must be 15 bits long'
    size = qr.shape[0]
    qr[8, size-8:] = format_bits[7:]
    qr[size-7:, 8] = format_bits[:7][::-1]
    qr[8, :6] = format_bits[:6]
    qr[8, 7:9] = format_bits[6:8]
    qr[7, 8] = format_bits[8]
    qr[:6, 8] = format_bits[9:15][::-1]
    return qr