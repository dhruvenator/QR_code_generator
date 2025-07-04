MODULE = {
    'black': 'D',
    'white': 'R',
    'reserved': 'U',
    'empty': 'V'
}

assert len(set(MODULE.values())) == len(MODULE), "These characters will be placed in the QR matrix so they must be unique."