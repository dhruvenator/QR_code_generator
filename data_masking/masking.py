from copy import deepcopy
from numpy import ndarray
from data_masking.penalty import PenaltyCalculator
from data_masking.mask_patterns import mask_pattern_appliers
from data_masking.version_format import add_version_information, add_format_information

class MaskEvaluator:
    def __init__(self, qr: ndarray, non_data_modules: list, version: int, error_correction: str):
        self.qr = qr
        self.non_data_modules = non_data_modules
        self.version = version
        self.error_correction = error_correction
        if self.version >= 7:
            self.qr = add_version_information(self.qr, self.version)
    
    def get_best_mask(self):
        min_penalty = float('inf')
        best_mask = None
        penalty_calculator = PenaltyCalculator()
        for masker in mask_pattern_appliers:
            masked_qr = masker.apply_mask(deepcopy(self.qr), self.non_data_modules)
            masked_qr = add_format_information(masked_qr, self.error_correction, masker.get_mask_id())
            penalty = penalty_calculator.calculate_penalty(masked_qr)
            if penalty < min_penalty:
                min_penalty = penalty
                best_mask = masked_qr
        return best_mask