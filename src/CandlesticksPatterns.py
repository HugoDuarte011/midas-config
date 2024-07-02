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

    # Convertendo o timestamp para datetime e preços para float
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)

    return df[['timestamp', 'open', 'high', 'low', 'close']]


# Função para identificar padrões de Martelo
def is_hammer(candle):
    body = abs(candle['close'] - candle['open'])
    lower_shadow = candle['open'] - candle['low'] if candle['close'] > candle['open'] else candle['close'] - candle[
        'low']
    upper_shadow = candle['high'] - candle['close'] if candle['close'] > candle['open'] else candle['high'] - candle[
        'open']

    return lower_shadow > 2 * body and upper_shadow < body


# Função para identificar padrões de Estrela da Manhã
def is_morning_star(candles):
    if len(candles) < 3:
        return False
    first, second, third = candles[-3], candles[-2], candles[-1]
    return (first['close'] < first['open'] and
            abs(second['close'] - second['open']) < (first['open'] - first['close']) / 2 and
            third['close'] > first['open'])


# Função para identificar padrões de Estrela Cadente
def is_shooting_star(candle):
    body = abs(candle['close'] - candle['open'])
    upper_shadow = candle['high'] - candle['close'] if candle['close'] > candle['open'] else candle['high'] - candle[
        'open']
    lower_shadow = candle['open'] - candle['low'] if candle['close'] > candle['open'] else candle['close'] - candle[
        'low']

    return upper_shadow > 2 * body and lower_shadow < body


# Função para identificar padrões de Nuvem Negra
def is_dark_cloud_cover(candles):
    if len(candles) < 2:
        return False
    first, second = candles[-2], candles[-1]
    return (first['close'] > first['open'] and
            second['open'] > first['high'] and
            second['close'] < first['open'] and
            second['close'] > first['close'])


# Função para identificar sinais de entrada com base nos padrões de candlestick
def identify_candlestick_patterns(df):
    df['Hammer'] = df.apply(lambda row: is_hammer(row), axis=1)
    df['Morning Star'] = df.apply(lambda row: is_morning_star(
        df[['open', 'high', 'low', 'close']].iloc[row.name - 2:row.name + 1].to_dict('records')), axis=1)
    df['Shooting Star'] = df.apply(lambda row: is_shooting_star(row), axis=1)
    df['Dark Cloud Cover'] = df.apply(lambda row: is_dark_cloud_cover(
        df[['open', 'high', 'low', 'close']].iloc[row.name - 1:row.name + 1].to_dict('records')), axis=1)

    return df


# Símbolos e intervalos de tempo desejados
symbols = ['BTCUSDT', 'ETHUSDT']
intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '4h', '12h', '1d', '1w']

# Iterar sobre cada símbolo e intervalo de tempo
for symbol in symbols:
    print(f"Analisando padrões de candlestick para o símbolo: {symbol}")
    for interval in intervals:
        print(f"Intervalo: {interval}")
        df = get_historical_klines(symbol, interval)

        # Identificar padrões de candlestick
        df = identify_candlestick_patterns(df)

        # Printar os padrões de candlestick
        print(df[['timestamp', 'Hammer', 'Morning Star', 'Shooting Star', 'Dark Cloud Cover']].tail(
            5))  # Mostra as últimas 5 entradas para visualização
        print("-" * 50)
