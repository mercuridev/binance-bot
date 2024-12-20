import pandas as pd
import logging
from strategies.rsi_strategy import calculate_rsi
from strategies.macd_strategy import calculate_macd
from strategies.sma_strategy import calculate_sma

def simulate_strategy(data: pd.DataFrame, strategy: str, config: dict):
    """
    Simulate a trading strategy on historical data.

    Parameters:
    - data: DataFrame containing historical market data.
    - strategy: Strategy name ('RSI', 'MACD', 'SMA').
    - config: Dictionary containing strategy configuration.

    Returns:
    - Simulated balance after running the strategy.
    """
    balance = config.get('initial_balance', 10000)
    holdings = 0
    for index in range(len(data)):
        # Apply selected strategy
        if strategy == 'RSI':
            data = calculate_rsi(data, config['rsi_period'])
            rsi = data['rsi'].iloc[index]
            if rsi < config['rsi_oversold']:
                if balance > 0:
                    holdings = balance / data['close'].iloc[index]
                    balance = 0
                    logging.info(f"BUY at {data['close'].iloc[index]} with RSI {rsi}")
            elif rsi > config['rsi_overbought']:
                if holdings > 0:
                    balance = holdings * data['close'].iloc[index]
                    holdings = 0
                    logging.info(f"SELL at {data['close'].iloc[index]} with RSI {rsi}")

        elif strategy == 'MACD':
            data = calculate_macd(data, config['fast_period'], config['slow_period'], config['signal_period'])
            macd = data['macd'].iloc[index]
            signal = data['signal_line'].iloc[index]
            if macd > signal and balance > 0:
                holdings = balance / data['close'].iloc[index]
                balance = 0
                logging.info(f"BUY at {data['close'].iloc[index]} with MACD {macd}")
            elif macd < signal and holdings > 0:
                balance = holdings * data['close'].iloc[index]
                holdings = 0
                logging.info(f"SELL at {data['close'].iloc[index]} with MACD {macd}")

        elif strategy == 'SMA':
            data = calculate_sma(data, config['short_window'], config['long_window'])
            sma_short = data['sma_short'].iloc[index]
            sma_long = data['sma_long'].iloc[index]
            if sma_short > sma_long and balance > 0:
                holdings = balance / data['close'].iloc[index]
                balance = 0
                logging.info(f"BUY at {data['close'].iloc[index]} with SMA short {sma_short}")
            elif sma_short < sma_long and holdings > 0:
                balance = holdings * data['close'].iloc[index]
                holdings = 0
                logging.info(f"SELL at {data['close'].iloc[index]} with SMA short {sma_short}")

    # Final balance
    if holdings > 0:
        balance = holdings * data['close'].iloc[-1]
    logging.info(f"Final balance: {balance}")
    return balance
