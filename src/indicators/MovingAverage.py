import pandas as pd

# Importar a nova classe BinanceDataFetcher
from src.dataFetching.BinanceDataFetcher import BinanceDataFetcher

# Configurações de exibição do pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Função para calcular médias móveis
def calculate_moving_averages(df, periods):
    for period in periods:
        df[f'SMA_{period}'] = df['close'].rolling(window=period).mean()
    return df

# Função para calcular médias móveis de 10 minutos a partir de dados de 5 minutos
def calculate_custom_interval(df, interval):
    if interval == '10m':
        df['timestamp'] = df['timestamp'].dt.floor('10T')
        custom_df = df.groupby('timestamp').agg({'close': 'mean'}).reset_index()
        return custom_df
    else:
        return df

# Função para identificar sinais de entrada (Golden Cross e Death Cross)
def identify_signals(df, short_period=12, long_period=26):
    df['SMA_Short'] = df[f'SMA_{short_period}']
    df['SMA_Long'] = df[f'SMA_{long_period}']

    df['Signal'] = 'None'
    for i in range(1, len(df)):
        if df['SMA_Short'].iloc[i - 1] < df['SMA_Long'].iloc[i - 1] and df['SMA_Short'].iloc[i] > df['SMA_Long'].iloc[i]:
            df.at[i, 'Signal'] = 'Long'
        elif df['SMA_Short'].iloc[i - 1] > df['SMA_Long'].iloc[i - 1] and df['SMA_Short'].iloc[i] < df['SMA_Long'].iloc[i]:
            df.at[i, 'Signal'] = 'Short'

    return df


# Símbolos e intervalos de tempo desejados
symbols = ['BTCUSDT', 'ETHUSDT']
intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '4h', '12h', '1d', '1w']
periods = [12, 26, 100, 200]

# Criar uma instância da classe BinanceDataFetcher
fetcher = BinanceDataFetcher(symbols, intervals)
fetcher.fetch_data()
data = fetcher.get_data()

# Iterar sobre cada símbolo e intervalo de tempo
for symbol in symbols:
    print(f"Calculando médias móveis para o símbolo: {symbol}")
    for interval in intervals:
        print(f"Intervalo: {interval}")
        df = data[symbol][interval]

        # Calcular médias móveis para outros intervalos
        df = calculate_moving_averages(df, periods)
        df = identify_signals(df)

        # Printando as médias móveis e sinais de entrada
        print(df.tail(5)[['timestamp', f'SMA_{12}', f'SMA_{26}', f'SMA_{100}', f'SMA_{200}',
                          'Signal']])  # Mostra as últimas 5 entradas para visualização
        print("-" * 50)
