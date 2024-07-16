import pandas as pd

# Importar a nova classe BinanceDataFetcher
from src.dataFetching.BinanceDataFetcher import BinanceDataFetcher

# Configurações de exibição do pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.options.display.float_format = '{:,.2f}'.format  # Formatação para evitar truncamento de grandes números

# Função para calcular o volume médio
def calculate_average_volume(df, period=20):
    df['Average Volume'] = df['volume'].rolling(window=period).mean()
    return df

# Função para identificar sinais de entrada com base no volume
def identify_volume_signals(df):
    df['Signal'] = 'None'
    for i in range(1, len(df)):
        if df['volume'].iloc[i] > df['Average Volume'].iloc[i] and df['close'].iloc[i] > df['close'].iloc[i-1]:
            df.at[i, 'Signal'] = 'Long'
        elif df['volume'].iloc[i] > df['Average Volume'].iloc[i] and df['close'].iloc[i] < df['close'].iloc[i-1]:
            df.at[i, 'Signal'] = 'Short'
    return df

# Símbolos e intervalos de tempo desejados
symbols = ['BTCUSDT', 'ETHUSDT']
intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '4h', '12h', '1d', '1w']
volume_period = 20  # Período padrão de 20 para o volume

# Criar uma instância da classe BinanceDataFetcher
fetcher = BinanceDataFetcher(symbols, intervals)
fetcher.fetch_data()
data = fetcher.get_data()

# Iterar sobre cada símbolo e intervalo de tempo
for symbol in symbols:
    print(f"Calculando volume para o símbolo: {symbol}")
    for interval in intervals:
        print(f"Intervalo: {interval}")
        df = data[symbol][interval]

        # Calcular o volume médio
        df = calculate_average_volume(df, volume_period)

        # Identificar sinais de volume
        df = identify_volume_signals(df)

        # Printar o volume e sinais de entrada
        print(df.tail(5)[['timestamp', 'volume', 'Average Volume', 'Signal']])  # Mostra as últimas 5 entradas para visualização
        print("-" * 50)
