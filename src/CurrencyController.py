class CurrencyController:
    def __init__(self):
        self.currencies = set()

    def add_currency(self, currency):
        self.currencies.add(currency)

    def remove_currency(self, currency):
        self.currencies.discard(currency)

    def get_currencies(self):
        return list(self.currencies)
