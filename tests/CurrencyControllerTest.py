import unittest
from src.CurrencyController import CurrencyController

class CurrencyControllerTest(unittest.TestCase):
    def setUp(self):
        self.controller = CurrencyController()

    def test_add_currency(self):
        self.controller.add_currency('BTC')
        self.assertIn('BTC', self.controller.currencies)

    def test_remove_currency(self):
        self.controller.add_currency('BTC')
        self.controller.remove_currency('BTC')
        self.assertNotIn('BTC', self.controller.currencies)

    def test_get_currencies(self):
        self.controller.add_currency('BTC')
        self.controller.add_currency('ETH')
        currencies = self.controller.get_currencies()
        self.assertEqual(len(currencies), 2)

if __name__ == '__main__':
    unittest.main()
