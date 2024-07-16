import unittest
import pandas as pd
from src.indicators.MovingAverage import MovingAverage
from src.indicators.BollingerBands import BollingerBands
from src.indicators.MACD import MACD
from src.indicators.RSI import RSI
from src.indicators.Volume import Volume
from src.indicators.CandlesticksPatterns import CandlesticksPatterns

class TestIndicators(unittest.TestCase):
    def setUp(self):
        data = {
            'timestamp': pd.date_range(start='1/1/2021', periods=5, freq='D'),
            'open': [1, 2, 3, 4, 5],
            'high': [2, 3, 4, 5, 6],
            'low': [0.5, 1.5, 2.5, 3.5, 4.5],
            'close': [1.5, 2.5, 3.5, 4.5, 5.5],
            'volume': [1000, 2000, 3000, 4000, 5000]
        }
        self.df = pd.DataFrame(data)
        self.df.set_index('timestamp', inplace=True)

    def test_moving_average(self):
        ma = MovingAverage(period=3)
        data = ma.calculate(self.df)
        self.assertIn('SMA3', data.columns)
        self.assertEqual(len(data['SMA3'].dropna()), 3)

    def test_bollinger_bands(self):
        bb = BollingerBands(period=3, std_dev=2)
        data = bb.calculate(self.df)
        self.assertIn('BollingerHigh', data.columns)
        self.assertIn('BollingerLow', data.columns)

    def test_macd(self):
        macd = MACD(fast_period=12, slow_period=26, signal_period=9)
        data = macd.calculate(self.df)
        self.assertIn('MACD', data.columns)
        self.assertIn('Signal', data.columns)

    def test_rsi(self):
        rsi = RSI(period=14)
        data = rsi.calculate(self.df)
        self.assertIn('RSI', data.columns)

    def test_volume(self):
        volume = Volume()
        data = volume.calculate(self.df)
        self.assertIn('Volume', data.columns)

    def test_candlestick_patterns(self):
        cp = CandlesticksPatterns()
        data = cp.hammer(self.df)
        self.assertIn('hammer', data.columns)
        data = cp.shootingStar(self.df)
        self.assertIn('shootingStar', data.columns)

if __name__ == '__main__':
    unittest.main()
