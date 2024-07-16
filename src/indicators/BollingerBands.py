import pandas as pd

# Importar a nova classe BinanceDataFetcher
from src.dataFetching.BinanceDataFetcher import BinanceDataFetcher

# Configurações de exibição do pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Função para calcular as Bandas de Bollinger
def calculate_bollinger_bands(df, period=20, std_dev=2):
    df['SMA'] = df['close'].rolling(window=period).mean()
    df['STD'] = df['close'].rolling(window=period).std()
    df['Upper Band'] = df['SMA'] + (df['STD'] * std_dev)
    df['Lower Band'] = df['SMA'] - (df['STD'] * std_dev)
    return df

# Função para identificar sinais de entrada
def identify_signals(df):
    df['Signal'] = 'None'
    for i in range(1, len(df)):
        if df['close'].iloc[i] <= df['Lower Band'].iloc[i]:
            df.at[i, 'Signal'] = 'Long'
        elif df['close'].iloc[i] >= df['Upper Band'].iloc[i]:
            df.at[i, 'Signal'] = 'Short'
    return df

# Símbolos e intervalos de tempo desejados
symbols = ['BTCUSDT', 'ETHUSDT']
intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '4h', '12h', '1d', '1w']

# Parâmetros para o cálculo das Bandas de Bollinger
period = 20
std_dev = 2

# Criar uma instância da classe BinanceDataFetcher
fetcher = BinanceDataFetcher(symbols, intervals)
fetcher.fetch_data()
data = fetcher.get_data()

# Iterar sobre cada símbolo e intervalo de tempo
for symbol in symbols:
    print(f"Calculando Bandas de Bollinger para o símbolo: {symbol}")
    for interval in intervals:
        print(f"Intervalo: {interval}")
        df = data[symbol][interval]

        # Calcular Bandas de Bollinger
        df = calculate_bollinger_bands(df, period, std_dev)

        # Identificar sinais de entrada
        df = identify_signals(df)

        # Printar as Bandas de Bollinger e sinais de entrada
        print(df.tail(5)[['timestamp', 'close', 'SMA', 'Upper Band', 'Lower Band', 'Signal']])  # Mostra as últimas 5 entradas para visualização
        print("-" * 50)
