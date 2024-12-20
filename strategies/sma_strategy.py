import logging
from binance.client import Client
import pandas as pd

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
        return data
    except Exception as e:
        logging.error(f"Failed to fetch historical data: {e}")
        raise

def calculate_sma(data: pd.DataFrame, short_window: int, long_window: int):
    """
    Calculate the Simple Moving Averages (SMA) for the given data.

    Parameters:
    - data: DataFrame containing price data.
    - short_window: Period for the short SMA.
    - long_window: Period for the long SMA.

    Returns:
    - DataFrame with SMA values added.
    """
    data['sma_short'] = data['close'].rolling(window=short_window).mean()
    data['sma_long'] = data['close'].rolling(window=long_window).mean()
    return data

def execute_sma_strategy(client: Client, symbol: str, config: dict):
    """
    Execute SMA trading strategy.

    Parameters:
    - client: Binance Client object.
    - symbol: Trading pair (e.g., BTCUSDT).
    - config: Dictionary containing strategy configuration.
    """
    try:
        logging.info(f"Executing SMA strategy for {symbol}...")

        # Fetch historical data
        data = fetch_historical_data(client, symbol, config['interval'], config['data_limit'])

        # Validate sufficient data for SMA calculation
        if len(data) < max(config['short_window'], config['long_window']):
            logging.error("Not enough data to calculate SMAs. Consider increasing 'data_limit'.")
            return

        # Calculate SMAs
        data = calculate_sma(data, config['short_window'], config['long_window'])

        # Get the latest SMA values
        latest_sma_short = data['sma_short'].iloc[-1]
        latest_sma_long = data['sma_long'].iloc[-1]

        # Make trading decision
        if latest_sma_short > latest_sma_long:
            logging.info(f"Short SMA ({latest_sma_short}) crossed above Long SMA ({latest_sma_long}). Buying {symbol}.")
            place_order(client, symbol, "BUY", config['order_size'])
        elif latest_sma_short < latest_sma_long:
            logging.info(f"Short SMA ({latest_sma_short}) crossed below Long SMA ({latest_sma_long}). Selling {symbol}.")
            place_order(client, symbol, "SELL", config['order_size'])
        else:
            logging.info("No clear SMA signal. Holding position.")

    except Exception as e:
        logging.error(f"Error in SMA strategy: {e}")
        raise
