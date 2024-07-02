import requests
import pandas as pd
import numpy as np
import time


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


# Função para calcular as Bandas de Bollinger
def calculate_bollinger_bands(df, period=20, std_dev=2):
    df['SMA'] = df['close'].rolling(window=period).mean()
    df['STD'] = df['close'].rolling(window=period).std()
    df['Upper Band'] = df['SMA'] + (df['STD'] * std_dev)
    df['Lower Band'] = df['SMA'] - (df['STD'] * std_dev)
    return df


# Função para identificar sinais de entrada
def identify_signals(df):
    last_row = df.iloc[-1]
    signals = {}
    if last_row['close'] <= last_row['Lower Band']:
        signals['Long'] = True
    else:
        signals['Long'] = False

    if last_row['close'] >= last_row['Upper Band']:
        signals['Short'] = True
    else:
        signals['Short'] = False

    return signals


# Símbolos e intervalos de tempo desejados
symbols = ['BTCUSDT', 'ETHUSDT']
intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '4h', '12h', '1d', '1w']

# Parâmetros para o cálculo das Bandas de Bollinger
period = 20
std_dev = 2

# Iterar sobre cada símbolo e intervalo de tempo
for symbol in symbols:
    print(f"Calculando Bandas de Bollinger para o símbolo: {symbol}")
    for interval in intervals:
        print(f"Intervalo: {interval}")
        df = get_historical_klines(symbol, interval)

        # Calcular Bandas de Bollinger
        df = calculate_bollinger_bands(df, period, std_dev)

        # Identificar sinais de entrada
        signals = identify_signals(df)

        # Printar as Bandas de Bollinger e sinais de entrada
        print(df[['timestamp', 'close', 'SMA', 'Upper Band', 'Lower Band']].tail(
            5))  # Mostra as últimas 5 entradas para visualização
        print(f"Sinal de Long: {'Sim' if signals['Long'] else 'Não'}")
        print(f"Sinal de Short: {'Sim' if signals['Short'] else 'Não'}")
        print("-" * 50)
        time.sleep(1)  # Para evitar ser bloqueado pela API devido a solicitações rápidas
