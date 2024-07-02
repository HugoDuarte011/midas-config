import requests
import pandas as pd


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

    if response.status_code != 200:
        raise Exception(f"Erro ao obter dados para {symbol} no intervalo {interval}: {data}")

    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['close'] = df['close'].astype(float)

    return df[['timestamp', 'close']]


# Função para calcular o MACD
def calculate_macd(df, short_period=12, long_period=26, signal_period=9):
    short_ema = df['close'].ewm(span=short_period, adjust=False).mean()
    long_ema = df['close'].ewm(span=long_period, adjust=False).mean()

    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    macd_histogram = macd_line - signal_line

    return macd_line, signal_line, macd_histogram


# Função para detectar cruzamentos MACD
def detect_macd_crossing(df):
    # Verifica se houve cruzamento nas duas últimas linhas
    if len(df) < 2:
        return None

    latest_row = df.iloc[-1]
    previous_row = df.iloc[-2]

    if previous_row['MACD_Line'] < previous_row['Signal_Line'] and latest_row['MACD_Line'] > latest_row['Signal_Line']:
        return 'Long'
    elif previous_row['MACD_Line'] > previous_row['Signal_Line'] and latest_row['MACD_Line'] < latest_row[
        'Signal_Line']:
        return 'Short'

    return None


# Símbolos e intervalos de tempo desejados
symbols = ['BTCUSDT', 'ETHUSDT']
intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '4h', '12h', '1d', '1w']


# Função principal para calcular o MACD e detectar cruzamentos
def inform_and_detect_macd_crossings():
    macd_crossings = {}

    for symbol in symbols:
        print(f"Calculando MACD para o símbolo: {symbol}")
        symbol_crossings = {}
        for interval in intervals:
            print(f"Intervalo: {interval}")
            try:
                df = get_historical_klines(symbol, interval)

                # Calcular o MACD
                macd_line, signal_line, macd_histogram = calculate_macd(df)
                df['MACD_Line'] = macd_line
                df['Signal_Line'] = signal_line
                df['MACD_Histogram'] = macd_histogram

                # Detectar cruzamentos
                crossing_signal = detect_macd_crossing(df)
                if crossing_signal:
                    last_cross_time = df.iloc[-1]['timestamp']
                    symbol_crossings[interval] = {
                        'crossing_signal': crossing_signal,
                        'time': last_cross_time
                    }

                # Exibir os últimos valores calculados
                print(df[['timestamp', 'close', 'MACD_Line', 'Signal_Line', 'MACD_Histogram']].tail(10))
                print("-" * 50)

            except Exception as e:
                print(e)

        if symbol_crossings:
            macd_crossings[symbol] = symbol_crossings

    print("Resumo dos cruzamentos MACD detectados:")
    print(macd_crossings)

    return macd_crossings


# Executar a função para calcular o MACD, detectar cruzamentos e informar
macd_crossings = inform_and_detect_macd_crossings()
