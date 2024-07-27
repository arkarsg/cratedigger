class TooManySourceException(Exception):
    def __init__(self, message="Provide only a URL or file upload"):
        self.message = message
        super().__init__(self.message)
