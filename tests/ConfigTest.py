import unittest
from src.Config import load_config

class ConfigTest(unittest.TestCase):
    def test_load_config(self):
        config = load_config()
        self.assertIsNotNone(config.BINANCE_API_KEY)
        self.assertIsNotNone(config.BINANCE_API_SECRET)

if __name__ == '__main__':
    unittest.main()