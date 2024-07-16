import requests
import pandas as pd

class BinanceDataFetcher:
    def __init__(self, symbols, intervals, limit=250):
        self.symbols = symbols
        self.intervals = intervals
        self.limit = limit
        self.data = {}

    def fetch_data(self):
        base_url = 'https://api.binance.com/api/v3/klines'
        for symbol in self.symbols:
            self.data[symbol] = {}
            for interval in self.intervals:
                params = {
                    'symbol': symbol,
                    'interval': interval,
                    'limit': self.limit
                }
                response = requests.get(base_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    df = pd.DataFrame(data, columns=[
                        'timestamp', 'open', 'high', 'low', 'close', 'volume',
                        'close_time', 'quote_asset_volume', 'number_of_trades',
                        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
                    ])
                    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                    df['open'] = df['open'].astype(float)
                    df['high'] = df['high'].astype(float)
                    df['low'] = df['low'].astype(float)
                    df['close'] = df['close'].astype(float)
                    df['volume'] = df['volume'].astype(float)
                    self.data[symbol][interval] = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
                else:
                    print(f"Erro ao obter dados para {symbol} no intervalo {interval}: {response.status_code}")

    def get_data(self):
        return self.data
