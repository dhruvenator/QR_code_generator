from numpy import ndarray, count_nonzero, select, array, sum as n_sum, all as n_all
from constants.qr_module_characters import MODULE
from numpy.lib.stride_tricks import sliding_window_view

class PenaltyCalculator:
    
    def _rule1(self) -> int:
        def row_penalty(arr: ndarray) -> int:
            total_penalty = 0
            for row in arr:
                current = row[0]
                count = 1
                for value in row[1:]:
                    if value == current:
                        count += 1
                    else:
                        if count >= 5:
                            total_penalty += 3 + (count - 5)
                        current = value
                        count = 1
                if count >= 5:
                    total_penalty += 3 + (count - 5)
            return total_penalty
        horizontal_penalty = row_penalty(self.matrix)
        vertical_penalty = row_penalty(self.matrix.T)
        return horizontal_penalty + vertical_penalty

    def _rule2(self) -> int:
        windows = sliding_window_view(self.matrix, (2, 2))
        sums = windows.sum(axis=(2, 3))
        count = count_nonzero((sums == -4) | (sums == 4))
        return count*3

    def _rule3(self) -> int:
        template = array([1, -1, 1, 1, 1, -1, 1, -1, -1, -1, -1])
        patterns = [template, template[::-1]]
        def count_pattern_in_rows(mat, pattern):
            views = sliding_window_view(mat, pattern.shape[0], axis=1)
            return n_sum(n_all(views == pattern, axis=2))
        total_matches = 0
        for pattern in patterns:
            total_matches += count_pattern_in_rows(self.matrix, pattern)
            total_matches += count_pattern_in_rows(self.matrix.T, pattern)
        return int(total_matches) * 40

    def _rule4(self) -> int:
        total_modules = self.matrix.shape[0] * self.matrix.shape[1]
        black_modules_count = count_nonzero(self.matrix == 1)
        percent_black = (black_modules_count / total_modules) * 100
        previous_5_multiple = (percent_black//5) * 5
        next_5_multiple = previous_5_multiple + 5
        return int(min(abs(previous_5_multiple - 50) // 5, abs(next_5_multiple - 50) // 5) * 10)

    def calculate_penalty(self, matrix: ndarray) -> int:
        self.matrix = matrix
        self.penalty = 0
        self.matrix = select(
            [self.matrix == MODULE['black'], self.matrix == MODULE['white']],
            [1, -1],
            default=0
        )
        self.penalty += self._rule1()
        self.penalty += self._rule2()
        self.penalty += self._rule3()
        self.penalty += self._rule4()
        return self.penalty