class GOSTBlockLengthError(Exception):
    def __str__(self):
        return f"Length of given block is not 32."