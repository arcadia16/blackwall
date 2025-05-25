class GOSTBlockLengthError(Exception):
    def __str__(self):
        return "Length of given block is not 32."
