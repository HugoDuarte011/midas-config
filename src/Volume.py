import requests
import pandas as pd
import numpy as np


# Função para obter dados históricos de preços da Binance, incluindo volume
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

    # Convertendo o timestamp para datetime e preços para float
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)

    return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]


# Função para identificar sinais de volume para Long e Short
def identify_volume_signals(df, volume_threshold=1.5):
    df['Change'] = df['close'].pct_change()
    df['Trend'] = np.where(df['Change'] > 0, 'Up', 'Down')

    avg_volume = df['volume'].rolling(window=20).mean()
    df['Volume Signal'] = np.where((df['volume'] > volume_threshold * avg_volume) & (df['Trend'] == 'Up'), 'Long',
                                   np.where((df['volume'] > volume_threshold * avg_volume) & (df['Trend'] == 'Down'),
                                            'Short', 'None'))
    return df


# Símbolos e intervalos de tempo desejados
symbols = ['BTCUSDT', 'ETHUSDT']
intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '4h', '12h', '1d', '1w']

# Iterar sobre cada símbolo e intervalo de tempo
for symbol in symbols:
    print(f"Analisando volumes de negociação para o símbolo: {symbol}")
    for interval in intervals:
        print(f"Intervalo: {interval}")
        df = get_historical_klines(symbol, interval)

        # Identificar sinais de volume para Long e Short
        df = identify_volume_signals(df)

        # Printar os sinais de volume
        print(df[['timestamp', 'volume', 'Volume Signal']].tail(5))  # Mostra as últimas 5 entradas para visualização
        print("-" * 50)
