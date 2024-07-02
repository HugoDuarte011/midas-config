import requests
import pandas as pd
import numpy as np


# Função para obter dados históricos de preços da Binance
def get_historical_klines(symbol, interval, limit=500):
    base_url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    # Convertendo os dados para DataFrame
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])

    # Convertendo o timestamp para datetime e fechando valores como float
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['close'] = df['close'].astype(float)

    return df[['timestamp', 'close']]


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

# Iterar sobre cada símbolo e intervalo de tempo
for symbol in symbols:
    print(f"Calculando RSI e MA do RSI para o símbolo: {symbol}")
    for interval in intervals:
        print(f"Intervalo: {interval}")
        df = get_historical_klines(symbol, interval)

        # Calcular RSI
        df = calculate_rsi(df, rsi_period)

        # Calcular a MA do RSI
        df = calculate_rsi_ma(df, f'RSI_{rsi_period}', rsi_ma_period)

        # Printar os valores do RSI e da MA do RSI
        print(df[['timestamp', f'RSI_{rsi_period}', f'RSI_MA_{rsi_ma_period}']].tail(
            5))  # Mostra as últimas 5 entradas para visualização
        print("-" * 50)
