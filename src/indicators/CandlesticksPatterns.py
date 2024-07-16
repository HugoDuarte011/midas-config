import pandas as pd

class CandlesticksPatterns:
    @staticmethod
    def hammer(data: pd.DataFrame):
        data['hammer'] = ((data['low'] < data['open']) & (data['low'] < data['close']) &
                          (data['close'] > data['open']) &
                          ((data['high'] - data['low']) > 2 * (data['open'] - data['low'])))
        return data

    @staticmethod
    def shootingStar(data: pd.DataFrame):
        data['shootingStar'] = ((data['high'] > data['open']) & (data['high'] > data['close']) &
                                 (data['close'] < data['open']) &
                                 ((data['high'] - data['low']) > 2 * (data['high'] - data['close'])))
        return data

# Example usage
# cp = CandlesticksPatterns()
# data = cp.hammer(data)
# data = cp.shootingStar(data)
# print(data.head())
