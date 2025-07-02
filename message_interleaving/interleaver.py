class MessageInterleaver:
    def __init__(self, groups, ec_codewords, version):
        self.groups = groups
        self.ec_codewords = ec_codewords
        self.version = version
        if len(groups) == 1:
            self.final_message = ''
        else:
            self.final_message = self._structure_message()
    
    def _structure_message(self):
        return ''