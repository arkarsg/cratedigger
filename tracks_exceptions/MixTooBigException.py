class MixTooBigException(Exception):
    def __init__(self, message="Mix too big! Upload mixes around 1h only"):
        self.message = message
        super().__init__(self.message)
