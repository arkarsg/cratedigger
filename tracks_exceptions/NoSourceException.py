class NoSourceException(Exception):
    def __init__(self, message="No URL or file upload provided"):
        self.message = message
        super().__init__(self.message)
