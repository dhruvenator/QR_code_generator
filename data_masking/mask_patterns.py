from abc import ABC, abstractmethod
from numpy import ndarray

class QRMasker(ABC):

    @abstractmethod
    def apply_mask(self, qr_matrix: ndarray, non_data_modules: list) -> ndarray:
        pass

    @abstractmethod
    def get_mask_id(self):
        pass

class MaskPattern1(QRMasker):
    def apply_mask(self, qr_matrix: ndarray, non_data_modules: list) -> ndarray:
        return qr_matrix
        for i in range(qr_matrix.shape[0]):
            for j in range(qr_matrix.shape[1]):
                if (i + j) % 2 == 0 and (i, j) not in non_data_modules:
                    qr_matrix[i][j] = 1 - qr_matrix[i][j]  # Flip the bit
        return qr_matrix

    def get_mask_id(self):
        return 0

class MaskPattern2(QRMasker):
    def apply_mask(self, qr_matrix: ndarray, non_data_modules: list) -> ndarray:
        return qr_matrix
        for i in range(qr_matrix.shape[0]):
            for j in range(qr_matrix.shape[1]):
                if i % 2 == 0 and (i, j) not in non_data_modules:
                    qr_matrix[i][j] = 1 - qr_matrix[i][j]  # Flip the bit
        return qr_matrix

    def get_mask_id(self):
        return 1

class MaskPattern3(QRMasker):
    def apply_mask(self, qr_matrix: ndarray, non_data_modules: list) -> ndarray:
        return qr_matrix
        for i in range(qr_matrix.shape[0]):
            for j in range(qr_matrix.shape[1]):
                if j % 3 == 0 and (i, j) not in non_data_modules:
                    qr_matrix[i][j] = 1 - qr_matrix[i][j]  # Flip the bit
        return qr_matrix

    def get_mask_id(self):
        return 2

class MaskPattern4(QRMasker):
    def apply_mask(self, qr_matrix: ndarray, non_data_modules: list) -> ndarray:
        return qr_matrix
        for i in range(qr_matrix.shape[0]):
            for j in range(qr_matrix.shape[1]):
                if (i + j) % 3 == 0 and (i, j) not in non_data_modules:
                    qr_matrix[i][j] = 1 - qr_matrix[i][j]  # Flip the bit
        return qr_matrix

    def get_mask_id(self):
        return 3

class MaskPattern5(QRMasker):
    def apply_mask(self, qr_matrix: ndarray, non_data_modules: list) -> ndarray:
        return qr_matrix
        for i in range(qr_matrix.shape[0]):
            for j in range(qr_matrix.shape[1]):
                if (i // 2 + j // 3) % 2 == 0 and (i, j) not in non_data_modules:
                    qr_matrix[i][j] = 1 - qr_matrix[i][j]  # Flip the bit
        return qr_matrix

    def get_mask_id(self):
        return 4

class MaskPattern6(QRMasker):
    def apply_mask(self, qr_matrix: ndarray, non_data_modules: list) -> ndarray:
        return qr_matrix
        for i in range(qr_matrix.shape[0]):
            for j in range(qr_matrix.shape[1]):
                if (i * j) % 2 == 0 and (i, j) not in non_data_modules:
                    qr_matrix[i][j] = 1 - qr_matrix[i][j]  # Flip the bit
        return qr_matrix

    def get_mask_id(self):
        return 5

class MaskPattern7(QRMasker):
    def apply_mask(self, qr_matrix: ndarray, non_data_modules: list) -> ndarray:
        return qr_matrix
        for i in range(qr_matrix.shape[0]):
            for j in range(qr_matrix.shape[1]):
                if (i + j) % 2 == 0 and (i, j) not in non_data_modules:
                    qr_matrix[i][j] = 1 - qr_matrix[i][j]  # Flip the bit
        return qr_matrix

    def get_mask_id(self):
        return 6

class MaskPattern8(QRMasker):
    def apply_mask(self, qr_matrix: ndarray, non_data_modules: list) -> ndarray:
        return qr_matrix
        for i in range(qr_matrix.shape[0]):
            for j in range(qr_matrix.shape[1]):
                if (i + j) % 3 == 0 and (i, j) not in non_data_modules:
                    qr_matrix[i][j] = 1 - qr_matrix[i][j]  # Flip the bit
        return qr_matrix

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