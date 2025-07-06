from numpy import ndarray, count_nonzero, select, array, tile
from constants.qr_module_characters import MODULE
from numpy.lib.stride_tricks import sliding_window_view
from data_masking.qr_21x21_char_matrix import test_qr

class PenaltyCalculator:
    
    def _rule1(self):
        
        ans = 0
        for i in range(len(self.matrix)):
            current_character = None
            current_count = 0
            j=-1

            while j<len(self.matrix[0]):
                j+=1
                if j>=len(self.matrix):
                    break
                if not current_character:
                    current_character = self.matrix[i][j]
                    current_count += 1
                
                else:
                    if self.matrix[i][j]==current_character:
                        current_count += 1
                        if current_count==5:
                            ans += 3
                        elif current_count >= 5:
                            ans+=1
                    
                    else:
                        current_character = self.matrix[i][j]
                        current_count = 1
        

        for j in range(len(self.matrix[0])):  # iterate over columns
            current_character = None
            current_count = 0
            i = -1

            while i < len(self.matrix):
                i += 1
                if i >= len(self.matrix):
                    break

                if not current_character:
                    current_character = self.matrix[i][j]
                    current_count = 1
                else:
                    if self.matrix[i][j] == current_character:
                        current_count += 1
                        if current_count == 5:
                            ans += 3
                        elif current_count > 5:
                            ans += 1
                    else:
                        current_character = self.matrix[i][j]
                        current_count = 1

        return ans




    def _rule2(self):
        windows = sliding_window_view(self.matrix, (2, 2))
        sums = windows.sum(axis=(2, 3))
        count = count_nonzero((sums == -4) | (sums == 4))
        return count*3



    def _rule3(self):

        pattern = array([1, -1, 1, 1, 1, -1, 1, -1, -1, -1, -1])
        k_len = len(pattern)

        total_matches = 0
        patterns = [pattern, pattern[::-1]]

        for arr in [self.matrix, self.matrix.T]:  # rowwise and columnwise
            if arr.shape[1] < k_len:
                continue  # skip if dimension too small

            windows = sliding_window_view(arr, window_shape=k_len, axis=1)  # shape (m, n-k+1, k)

            for p in patterns:
                K = tile(p, (arr.shape[0], 1))                      # shape (m, k)
                matches = (windows == K[:, None, :])                # shape (m, n-k+1, k)
                full_match_mask = matches.all(axis=2)               # True where full match
                total_matches += full_match_mask.sum()

        return int(total_matches) * 40

    def _rule4(self):
        total_modules = self.matrix.shape[0]*self.matrix.shape[1]
        black_modules_count = count_nonzero(self.matrix == 1)
        white_module_count = count_nonzero(self.matrix==-1)
        percent_black = (black_modules_count)*100/(total_modules)
        previous_5_multiple = (percent_black//5)*5
        next_5_multiple = (percent_black//5 + 1)*5
        return int(min(abs(previous_5_multiple-50)//5, abs(next_5_multiple-50)//5)*10)



    def calculate_penalty(self, matrix: ndarray):
        self.matrix = test_qr
        self.matrix = select(
                [self.matrix == 'D', self.matrix == 'R'],
                [1, -1],
                default=0
            )

        self.penalty = 0
        rule_1_count = self._rule1()
        print('rule_1_count', rule_1_count)
        rule_2_count = self._rule2()
        print('rule 2 count', rule_2_count)
        rule_3_count = self._rule3()
        print('rule 3 count', rule_3_count)
        rule_4_count = self._rule4()
        print('rule_4_count', rule_4_count)
        return matrix