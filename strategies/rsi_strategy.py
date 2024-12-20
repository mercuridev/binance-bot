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

def calculate_rsi(data: pd.DataFrame, period: int):
    """
    Calculate the Relative Strength Index (RSI) for the given data.

    Parameters:
    - data: DataFrame containing price data.
    - period: Period for the RSI calculation.

    Returns:
    - DataFrame with RSI values added.
    """
    delta = data['close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    rs = avg_gain / avg_loss
    data['rsi'] = 100 - (100 / (1 + rs))

    return data

def execute_rsi_strategy(client: Client, symbol: str, config: dict):
    """
    Execute RSI trading strategy.

    Parameters:
    - client: Binance Client object.
    - symbol: Trading pair (e.g., BTCUSDT).
    - config: Dictionary containing strategy configuration.
    """
    try:
        logging.info(f"Executing RSI strategy for {symbol}...")

        # Fetch historical data
        data = fetch_historical_data(client, symbol, config['interval'], config['data_limit'])

        # Validate sufficient data for RSI calculation
        if len(data) < config['rsi_period']:
            logging.error("Not enough data to calculate RSI. Consider increasing 'data_limit'.")
            return

        # Calculate RSI
        data = calculate_rsi(data, config['rsi_period'])

        # Get the latest RSI value
        latest_rsi = data['rsi'].iloc[-1]

        # Make trading decision
        if latest_rsi < config['rsi_oversold']:
            logging.info(f"RSI ({latest_rsi}) below {config['rsi_oversold']}. Buying {symbol}.")
            place_order(client, symbol, "BUY", config['order_size'])
        elif latest_rsi > config['rsi_overbought']:
            logging.info(f"RSI ({latest_rsi}) above {config['rsi_overbought']}. Selling {symbol}.")
            place_order(client, symbol, "SELL", config['order_size'])
        else:
            logging.info(f"RSI ({latest_rsi}) neutral. Holding position.")

    except Exception as e:
        logging.error(f"Error in RSI strategy: {e}")
        raise
