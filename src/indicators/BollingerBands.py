import pandas as pd

class BollingerBands:
    def __init__(self, period=20, std_dev=2):
        self.period = period
        self.std_dev = std_dev

    def calculate(self, data: pd.DataFrame):
        data['SMA'] = data['close'].rolling(window=self.period).mean()
        data['BollingerHigh'] = data['SMA'] + (data['close'].rolling(window=self.period).std() * self.std_dev)
        data['BollingerLow'] = data['SMA'] - (data['close'].rolling(window=self.period).std() * self.std_dev)
        return data

# Example usage
# bb = BollingerBands()
# data = bb.calculate(data)
# print(data[['close', 'BollingerHigh', 'BollingerLow']].head())
