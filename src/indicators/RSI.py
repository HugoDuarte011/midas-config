import pandas as pd

# Importar a nova classe BinanceDataFetcher
from src.dataFetching.BinanceDataFetcher import BinanceDataFetcher

# Configurações de exibição do pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Função para calcular o RSI usando lógica de média móvel suavizada (SMMA)
def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # Inicializa a média móvel suavizada (SMMA) com a média simples dos primeiros `period` valores
    avg_gain = gain.rolling(window=period).mean().shift(1)
    avg_loss = loss.rolling(window=period).mean().shift(1)

    avg_gain.iloc[period] = gain.iloc[1:period + 1].mean()
    avg_loss.iloc[period] = loss.iloc[1:period + 1].mean()

    # Calcula SMMA para o restante dos dados
    for i in range(period + 1, len(gain)):
        avg_gain.iloc[i] = (avg_gain.iloc[i - 1] * (period - 1) + gain.iloc[i]) / period
        avg_loss.iloc[i] = (avg_loss.iloc[i - 1] * (period - 1) + loss.iloc[i]) / period

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    df[f'RSI_{period}'] = rsi

    # Identificar sinais de Long e Short
    df['Signal'] = 'None'
    df.loc[df[f'RSI_{period}'] < 30, 'Signal'] = 'Long'
    df.loc[df[f'RSI_{period}'] > 70, 'Signal'] = 'Short'

    return df

# Função para calcular a Média Móvel do RSI
def calculate_rsi_ma(df, rsi_column, ma_period=14):
    df[f'RSI_MA_{ma_period}'] = df[rsi_column].rolling(window=ma_period).mean()
    return df

# Símbolos e intervalos de tempo desejados
symbols = ['BTCUSDT', 'ETHUSDT']
intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '4h', '12h', '1d', '1w']
rsi_period = 14  # Período padrão de 14 para o RSI
rsi_ma_period = 14  # Período padrão de 14 para a MA do RSI

# Criar uma instância da classe BinanceDataFetcher
fetcher = BinanceDataFetcher(symbols, intervals)
fetcher.fetch_data()
data = fetcher.get_data()

# Iterar sobre cada símbolo e intervalo de tempo
for symbol in symbols:
    print(f"Calculando RSI e MA do RSI para o símbolo: {symbol}")
    for interval in intervals:
        print(f"Intervalo: {interval}")
        df = data[symbol][interval]

        # Calcular RSI
        df = calculate_rsi(df, rsi_period)

        # Calcular a MA do RSI
        df = calculate_rsi_ma(df, f'RSI_{rsi_period}', rsi_ma_period)

        # Printar os valores do RSI, da MA do RSI e dos sinais
        print(df.tail(5)[['timestamp', f'RSI_{rsi_period}', f'RSI_MA_{rsi_ma_period}', 'Signal']])  # Mostra as últimas 5 entradas para visualização
        print("-" * 50)
