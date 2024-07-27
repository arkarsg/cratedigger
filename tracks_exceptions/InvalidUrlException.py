class InvalidUrlException(Exception):
    def __init__(self, message="URL is invalid"):
        self.message = message
        super().__init__(self.message)
