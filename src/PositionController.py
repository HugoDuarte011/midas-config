class PositionController:
    def __init__(self):
        self.positions = {}

    def add_position(self, currency, position):
        self.positions[currency] = position

    def remove_position(self, currency):
        if currency in self.positions:
            del self.positions[currency]

    def get_positions(self):
        return self.positions
