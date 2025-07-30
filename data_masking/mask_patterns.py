from abc import ABC, abstractmethod
from numpy import ndarray, indices, stack, array
from constants.qr_module_characters import MODULE

class QRMasker(ABC):

    @abstractmethod
    def mask_pattern(self, rows: ndarray, cols: ndarray) -> ndarray:
        pass

    def apply_mask(self, qr_matrix: ndarray, non_data_modules: list) -> ndarray:
        non_data_set = set(non_data_modules)
        rows, cols = indices(qr_matrix.shape)
        # Get the mask basd on the mask pattern
        pattern_mask = self.mask_pattern(rows, cols)
        all_indices = stack((rows, cols), axis=-1).reshape(-1, 2)
        # Create a mask for data modules
        data_mask = array([tuple(idx) not in non_data_set for idx in all_indices])
        data_mask = data_mask.reshape(qr_matrix.shape)
        # Flip the data modules based on the mask pattern
        flip_mask = pattern_mask & data_mask
        black, white = MODULE['black'], MODULE['white']
        swap_black_to_white = (qr_matrix == black) & flip_mask
        swap_white_to_black = (qr_matrix == white) & flip_mask
        qr_matrix[swap_black_to_white] = white
        qr_matrix[swap_white_to_black] = black
        return qr_matrix

    @abstractmethod
    def get_mask_id(self):
        pass

class MaskPattern1(QRMasker):
    def mask_pattern(self, rows: ndarray, cols: list) -> ndarray:
        return (rows + cols) % 2 == 0

    def get_mask_id(self):
        return 0

class MaskPattern2(QRMasker):
    def mask_pattern(self, rows: ndarray, cols: list) -> ndarray:
        return rows % 2 == 0

    def get_mask_id(self):
        return 1

class MaskPattern3(QRMasker):
    def mask_pattern(self, rows: ndarray, cols: list) -> ndarray:
        return cols % 3 == 0

    def get_mask_id(self):
        return 2

class MaskPattern4(QRMasker):
    def mask_pattern(self, rows: ndarray, cols: list) -> ndarray:
        return (rows + cols) % 3 == 0

    def get_mask_id(self):
        return 3

class MaskPattern5(QRMasker):
    def mask_pattern(self, rows: ndarray, cols: list) -> ndarray:
        return (rows//2 + cols//3) % 2 == 0

    def get_mask_id(self):
        return 4

class MaskPattern6(QRMasker):
    def mask_pattern(self, rows: ndarray, cols: list) -> ndarray:
        return ((rows * cols) % 2) + ((rows * cols) % 3) == 0

    def get_mask_id(self):
        return 5

class MaskPattern7(QRMasker):
    def mask_pattern(self, rows: ndarray, cols: list) -> ndarray:
        return (((rows * cols) % 2) + ((rows * cols) % 3)) % 2 == 0

    def get_mask_id(self):
        return 6

class MaskPattern8(QRMasker):
    def mask_pattern(self, rows: ndarray, cols: list) -> ndarray:
        return (((rows + cols) % 2) + ((rows * cols) % 3)) % 2 == 0

    def get_mask_id(self):
        return 7

mask_pattern_appliers = [
    MaskPattern1(),
    MaskPattern2(),
    MaskPattern3(),
    MaskPattern4(),
    MaskPattern5(),
    MaskPattern6(),
    MaskPattern7(),
    MaskPattern8()
]