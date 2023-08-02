

class InvalidSenderEmail(Exception):
    def __init__(self, receiver):
        self.receiver = receiver
        self.message = f"The email {self.receiver} isn't correct"
        super().__init__(self.message)