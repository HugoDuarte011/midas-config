import unittest
import pandas as pd
from src.dataFetching.BinanceDataFetcher import BinanceDataFetcher

class TestBinanceDataFetcher(unittest.TestCase):
    def test_fetch_klines(self):
        fetcher = BinanceDataFetcher('BTCUSDT', '1h')
        data = fetcher.fetchKlines(limit=5)
        expected_columns = ['open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseAssetVolume', 'takerBuyQuoteAssetVolume', 'ignore']
        self.assertEqual(len(data), 5)
        self.assertTrue(all(column in data.columns for column in expected_columns))
        pd.set_option('display.max_columns', None)
        print(data)

if __name__ == '__main__':
    unittest.main()
