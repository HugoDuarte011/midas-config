import logging
import yaml
import pandas as pd
from dataFetching.BinanceDataFetcher import BinanceDataFetcher
from indicators.MovingAverage import MovingAverage
from indicators.BollingerBands import BollingerBands
from indicators.MACD import MACD
from indicators.RSI import RSI
from indicators.Volume import Volume

# Load config
def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

config = load_config('config.yaml')

# Setup logging
logging.basicConfig(level=config['logging']['level'], filename=config['logging']['file'], filemode='a', format='%(name)s - %(levelname)s - %(message)s')

# Fetch data
fetcher = BinanceDataFetcher('BTCUSDT', '1h')
data = fetcher.fetchKlines(limit=100)

# Calculate indicators
ma = MovingAverage(period=14)
data = ma.calculate(data)

bb = BollingerBands(period=20, std_dev=2)
data = bb.calculate(data)

macd = MACD(fast_period=12, slow_period=26, signal_period=9)
data = macd.calculate(data)

rsi = RSI(period=14)
data = rsi.calculate(data)

volume = Volume()
data = volume.calculate(data)

pd.set_option('display.max_columns', None)
print(data.head())
