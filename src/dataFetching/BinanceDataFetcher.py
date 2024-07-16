import requests
import pandas as pd

class BinanceDataFetcher:
    BASE_URL = "https://api.binance.com"

    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval

    def fetchKlines(self, limit=100):
        url = f"{self.BASE_URL}/api/v3/klines"
        params = {
            'symbol': self.symbol,
            'interval': self.interval,
            'limit': limit
        }
        response = requests.get(url, params=params)
        data = response.json()
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseAssetVolume', 'takerBuyQuoteAssetVolume', 'ignore'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        # Convert relevant columns to numeric types
        numeric_columns = ['open', 'high', 'low', 'close', 'volume', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseAssetVolume', 'takerBuyQuoteAssetVolume']
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

        return df

# Example usage
# fetcher = BinanceDataFetcher('BTCUSDT', '1h')
# data = fetcher.fetchKlines()
# pd.set_option('display.max_columns', None)
# print(data.head())
