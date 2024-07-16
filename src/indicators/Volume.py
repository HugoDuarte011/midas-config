import pandas as pd

class Volume:
    def calculate(self, data: pd.DataFrame):
        data['Volume'] = data['volume']
        return data

# Example usage
# volume = Volume()
# data = volume.calculate(data)
# print(data[['close', 'Volume']].head())
