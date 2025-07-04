from numpy import full, all, tile
from constants.qr_alignment_pattern_locations import ALIGNMENT_PATTERN_LOCATIONS
from constants.qr_module_characters import MODULE

class ModulePlacer:
    def __init__(self, version: int):
        self.version = version
        self.size = (self.version - 1) * 4 + 21
        self.qr = full((self.size, self.size), MODULE['empty'])
        self._add_finder_patterns()
        self._add_seperators()
        self._add_alignment_patterns()
        self._add_timing_patterns()
        self._add_dark_module()
        self._reserve_modules()
    
    def _add_finder_patterns(self):
        def draw_pattern(x: int, y: int):
            self.qr[x:x+7, y:y+7] = MODULE['black']
            self.qr[x+1:x+6, y+1:y+6] = MODULE['white']
            self.qr[x+2:x+5, y+2:y+5] = MODULE['black']
        draw_pattern(0, 0)
        draw_pattern(self.size - 7, 0)
        draw_pattern(0, self.size - 7)

    def _add_seperators(self):
        def draw_pattern(i: int, j: int):
            if i > 4:
                self.qr[i-4, j-3:j+4] = MODULE['white']
            if i < self.size - 4:
                self.qr[i+4, j-3:j+4] = MODULE['white']
            if j > 4:
                self.qr[max(i-4, 0):min(i+5, self.size), j-4] = MODULE['white']
            if j < self.size - 4:
                self.qr[max(i-4, 0):min(i+5, self.size), j+4] = MODULE['white']
        draw_pattern(3, 3)
        draw_pattern(3, self.size - 4)
        draw_pattern(self.size - 4, 3)

    def _add_alignment_patterns(self):
        center_locations = ALIGNMENT_PATTERN_LOCATIONS[self.version]
        def draw_pattern(cx: int, cy: int):
            self.qr[cx-2:cx+3, cy-2:cy+3] = MODULE['black']
            self.qr[cx-1:cx+2, cy-1:cy+2] = MODULE['white']
            self.qr[cx, cy] = MODULE['black']
        for x in center_locations:
            for y in center_locations:
                region = self.qr[x-2:x+3, y-2:y+3]
                if all(region == None):
                    draw_pattern(x, y)

    def _add_timing_patterns(self):
        pattern_length = self.size - 16
        timing_pattern = tile([MODULE['black'], MODULE['white']], pattern_length // 2 + 1)[:pattern_length]
        self.qr[6, 8:self.size-8] = timing_pattern
        self.qr[8:self.size-8, 6] = timing_pattern.T

    def _add_dark_module(self):
        self.qr[self.size-8, 8] = MODULE['black']
    
    def _reserve_modules(self):
        def reserve_format_information_area():
            self.qr[8, self.size-8:] = MODULE['reserved']
            self.qr[self.size-7:, 8] = MODULE['reserved']
            self.qr[8, :6] = MODULE['reserved']
            self.qr[8, 7:9] = MODULE['reserved']
            self.qr[:6, 8] = MODULE['reserved']
            self.qr[7, 8] = MODULE['reserved']
        def reserve_version_information_area():
            self.qr[:6, self.size-11:self.size-8] = MODULE['reserved']
            self.qr[self.size-11:self.size-8, :6] = MODULE['reserved']
        reserve_format_information_area()
        if self.version >= 7:
            reserve_version_information_area()

    def place_data_bits(self, data):
        return self.qr