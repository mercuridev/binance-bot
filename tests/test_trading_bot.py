import pytest
from unittest.mock import MagicMock
import pandas as pd
from strategies.rsi_strategy import calculate_rsi
from strategies.macd_strategy import calculate_macd
from strategies.sma_strategy import calculate_sma
from orders.orders_manager import place_order, get_account_balance

# Sample DataFrame for testing
def get_sample_data():
    data = {
        'close': [100, 102, 101, 103, 104, 102, 100, 99, 98, 97],
        'open': [99, 101, 100, 102, 103, 101, 99, 98, 97, 96],
        'high': [102, 103, 102, 104, 105, 103, 101, 100, 99, 98],
        'low': [98, 100, 99, 101, 102, 100, 98, 97, 96, 95],
        'volume': [1000, 1200, 1100, 1300, 1400, 1200, 1000, 900, 800, 700]
    }
    return pd.DataFrame(data)

# Test RSI Calculation
def test_calculate_rsi():
    data = get_sample_data()
    rsi_period = 14
    data_with_rsi = calculate_rsi(data, rsi_period)
    assert 'rsi' in data_with_rsi.columns
    assert data_with_rsi['rsi'].notnull().sum() > 0

# Test MACD Calculation
def test_calculate_macd():
    data = get_sample_data()
    fast_period, slow_period, signal_period = 12, 26, 9
    data_with_macd = calculate_macd(data, fast_period, slow_period, signal_period)
    assert 'macd' in data_with_macd.columns
    assert 'signal_line' in data_with_macd.columns
    assert data_with_macd['macd'].notnull().sum() > 0
    assert data_with_macd['signal_line'].notnull().sum() > 0

# Test SMA Calculation
def test_calculate_sma():
    data = get_sample_data()
    short_window, long_window = 3, 5
    data_with_sma = calculate_sma(data, short_window, long_window)
    assert 'sma_short' in data_with_sma.columns
    assert 'sma_long' in data_with_sma.columns
    assert data_with_sma['sma_short'].notnull().sum() > 0
    assert data_with_sma['sma_long'].notnull().sum() > 0

# Test Place Order Mock
def test_place_order():
    client_mock = MagicMock()
    client_mock.create_order.return_value = {
        'orderId': '12345',
        'status': 'FILLED',
        'symbol': 'BTCUSDT'
    }
    order = place_order(client_mock, 'BTCUSDT', 'BUY', 0.01)
    assert order['orderId'] == '12345'
    assert order['status'] == 'FILLED'

# Test Get Account Balance Mock
def test_get_account_balance():
    client_mock = MagicMock()
    client_mock.get_account.return_value = {
        'balances': [
            {'asset': 'BTC', 'free': '0.5'},
            {'asset': 'USDT', 'free': '1000'}
        ]
    }
    balance = get_account_balance(client_mock, 'BTC')
    assert balance == 0.5
