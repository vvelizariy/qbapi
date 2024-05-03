class QBAPIException(Exception):
    def __init__(self, message="Request to QB API failed"):
        self.message = message
        super().__init__(self.message)
