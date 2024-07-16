import pandas as pd

class RSI:
    def __init__(self, period=14):
        self.period = period

    def calculate(self, data: pd.DataFrame):
        delta = data['close'].diff(1)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=self.period).mean()
        avg_loss = loss.rolling(window=self.period).mean()
        rs = avg_gain / avg_loss
        data['RSI'] = 100 - (100 / (1 + rs))
        return data

# Example usage
# rsi = RSI()
# data = rsi.calculate(data)
# print(data[['close', 'RSI']].head())
