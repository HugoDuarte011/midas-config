import pandas as pd

class MovingAverage:
    def __init__(self, period=14):
        self.period = period

    def calculate(self, data: pd.DataFrame):
        data[f'SMA{self.period}'] = data['close'].rolling(window=self.period).mean()
        return data

# Example usage
# ma = MovingAverage()
# data = ma.calculate(data)
# print(data[['close', f'SMA{self.period}']].head())
