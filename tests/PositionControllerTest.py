import unittest
from src.PositionController import PositionController

class PositionControllerTest(unittest.TestCase):
    def setUp(self):
        self.controller = PositionController()

    def test_add_position(self):
        self.controller.add_position('BTC', 'long')
        self.assertIn('BTC', self.controller.positions)
        self.assertEqual(self.controller.positions['BTC'], 'long')

    def test_remove_position(self):
        self.controller.add_position('BTC', 'long')
        self.controller.remove_position('BTC')
        self.assertNotIn('BTC', self.controller.positions)

    def test_get_positions(self):
        self.controller.add_position('BTC', 'long')
        self.controller.add_position('ETH', 'short')
        positions = self.controller.get_positions()
        self.assertEqual(len(positions), 2)

if __name__ == '__main__':
    unittest.main()
