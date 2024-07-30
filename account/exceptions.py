class NotEnoughMoney(Exception):
    def __init__(self, message="Not enough money to complete the transaction"):
        self.message = message
        super().__init__(self.message)

class InvalidQuantity(Exception):
    def __init__(self, message="Invalid quantity for the transaction"):
        self.message = message
        super().__init__(self.message)