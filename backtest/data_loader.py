import pandas as pd
import os
import logging

def load_historical_data(filepath: str):
    """
    Load historical market data from a CSV file.

    Parameters:
    - filepath: Path to the CSV file containing historical data.

    Returns:
    - DataFrame containing the historical data.
    """
    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}")
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        data = pd.read_csv(filepath)
        data['close'] = data['close'].astype(float)
        data['open'] = data['open'].astype(float)
        data['high'] = data['high'].astype(float)
        data['low'] = data['low'].astype(float)
        data['volume'] = data['volume'].astype(float)
        logging.info(f"Data loaded successfully from {filepath}.")
        return data
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise
