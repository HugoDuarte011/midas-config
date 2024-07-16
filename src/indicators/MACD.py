import pandas as pd

class MACD:
    def __init__(self, fast_period=12, slow_period=26, signal_period=9):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

    def calculate(self, data: pd.DataFrame):
        data['MACD'] = data['close'].ewm(span=self.fast_period, adjust=False).mean() - data['close'].ewm(span=self.slow_period, adjust=False).mean()
        data['Signal'] = data['MACD'].ewm(span=self.signal_period, adjust=False).mean()
        return data

# Example usage
# macd = MACD()
# data = macd.calculate(data)
# print(data[['close', 'MACD', 'Signal']].head())
