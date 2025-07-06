from numpy import ndarray
from data_masking.penalty import PenaltyCalculator

class MaskEvaluator:
    def __init__(self, qr: ndarray, non_data_modules: list):
        self.qr = qr
        self.non_data_modules = non_data_modules
    
    def get_best_mask(self):
        penalty_calculator = PenaltyCalculator()
        penalty_calculator.calculate_penalty(self.qr)