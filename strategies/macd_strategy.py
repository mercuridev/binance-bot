import logging
from binance.client import Client
import pandas as pd
import numpy as np
from orders.orders_manager import place_order

def fetch_historical_data(client: Client, symbol: str, interval: str, limit: int):
    """
    Fetch historical candlestick data from Binance.

    Parameters:
    - client: Binance Client object.
    - symbol: Trading pair (e.g., BTCUSDT).
    - interval: Kline interval (e.g., 1h, 4h, 1d).
    - limit: Number of candles to fetch.

    Returns:
    - DataFrame containing historical data.
    """
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        data = pd.DataFrame(klines, columns=[
            'open_time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        data['close'] = data['close'].astype(float)
        data['open'] = data['open'].astype(float)
        data['high'] = data['high'].astype(float)
        data['low'] = data['low'].astype(float)
        data['volume'] = data['volume'].astype(float)
        return data
    except Exception as e:
        logging.error(f"Failed to fetch historical data: {e}")
        raise

def calculate_macd(data: pd.DataFrame, fast_period: int, slow_period: int, signal_period: int):
    """
    Calculate MACD and Signal Line for the given data.

    Parameters:
    - data: DataFrame containing price data.
    - fast_period: Period for the fast EMA.
    - slow_period: Period for the slow EMA.
    - signal_period: Period for the signal line EMA.

    Returns:
    - DataFrame with MACD and Signal Line added.
    """
    data['ema_fast'] = data['close'].ewm(span=fast_period, adjust=False).mean()
    data['ema_slow'] = data['close'].ewm(span=slow_period, adjust=False).mean()
    data['macd'] = data['ema_fast'] - data['ema_slow']
    data['signal_line'] = data['macd'].ewm(span=signal_period, adjust=False).mean()
    return data

def execute_macd_strategy(client: Client, symbol: str, config: dict):
    """
    Execute MACD trading strategy.

    Parameters:
    - client: Binance Client object.
    - symbol: Trading pair (e.g., BTCUSDT).
    - config: Dictionary containing strategy configuration.
    """
    try:
        logging.info(f"Executing MACD strategy for {symbol}...")

        # Fetch historical data
        data = fetch_historical_data(client, symbol, config['interval'], config['data_limit'])

        # Validate sufficient data for MACD calculation
        if len(data) < max(config['fast_period'], config['slow_period'], config['signal_period']):
            logging.error("Not enough data to calculate MACD. Consider increasing 'data_limit'.")
            return

        # Calculate MACD and Signal Line
        data = calculate_macd(data, config['fast_period'], config['slow_period'], config['signal_period'])

        # Get the latest MACD and Signal Line values
        latest_macd = data['macd'].iloc[-1]
        latest_signal = data['signal_line'].iloc[-1]

        # Make trading decision
        if latest_macd > latest_signal:
            logging.info(f"MACD ({latest_macd}) crossed above Signal Line ({latest_signal}). Buying {symbol}.")
            place_order(client, symbol, "BUY", config['order_size'])
        elif latest_macd < latest_signal:
            logging.info(f"MACD ({latest_macd}) crossed below Signal Line ({latest_signal}). Selling {symbol}.")
            place_order(client, symbol, "SELL", config['order_size'])
        else:
            logging.info("No clear MACD signal. Holding position.")

    except Exception as e:
        logging.error(f"Error in MACD strategy: {e}")
        raise
