import pandas as pd

# Importar a nova classe BinanceDataFetcher
from src.dataFetching.BinanceDataFetcher import BinanceDataFetcher

# Configurações de exibição do pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Função para calcular o MACD
def calculate_macd(df, short_period=12, long_period=26, signal_period=9):
    short_ema = df['close'].ewm(span=short_period, adjust=False).mean()
    long_ema = df['close'].ewm(span=long_period, adjust=False).mean()

    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    macd_histogram = macd_line - signal_line

    df['MACD_Line'] = macd_line
    df['Signal_Line'] = signal_line
    df['MACD_Histogram'] = macd_histogram

    return df

# Função para identificar sinais de entrada
def identify_signals(df):
    df['Signal'] = 'None'
    for i in range(1, len(df)):
        if df['MACD_Line'].iloc[i] > df['Signal_Line'].iloc[i] and df['MACD_Line'].iloc[i - 1] <= df['Signal_Line'].iloc[i - 1]:
            df.at[i, 'Signal'] = 'Long'
        elif df['MACD_Line'].iloc[i] < df['Signal_Line'].iloc[i] and df['MACD_Line'].iloc[i - 1] >= df['Signal_Line'].iloc[i - 1]:
            df.at[i, 'Signal'] = 'Short'
    return df

# Símbolos e intervalos de tempo desejados
symbols = ['BTCUSDT', 'ETHUSDT']
intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '4h', '12h', '1d', '1w']

# Criar uma instância da classe BinanceDataFetcher
fetcher = BinanceDataFetcher(symbols, intervals)
fetcher.fetch_data()
data = fetcher.get_data()

# Iterar sobre cada símbolo e intervalo de tempo
for symbol in symbols:
    print(f"Calculando MACD para o símbolo: {symbol}")
    for interval in intervals:
        print(f"Intervalo: {interval}")
        df = data[symbol][interval]

        # Calcular o MACD
        df = calculate_macd(df)

        # Identificar sinais de entrada
        df = identify_signals(df)

        # Printar o MACD e sinais de entrada
        print(df.tail(5)[['timestamp', 'close', 'MACD_Line', 'Signal_Line', 'MACD_Histogram', 'Signal']])  # Mostra as últimas 5 entradas para visualização
        print("-" * 50)
