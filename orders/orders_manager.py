import logging
from binance.client import Client

# Order Manager for handling Binance trades
def place_order(client: Client, symbol: str, side: str, quantity: float, price: float = None):
    """
    Places an order on Binance.

    Parameters:
    - client: Binance Client object.
    - symbol: Trading pair (e.g., BTCUSDT).
    - side: BUY or SELL.
    - quantity: Quantity to trade.
    - price: Optional limit price for LIMIT orders.

    Returns:
    - Order response from Binance.
    """
    try:
        if price:
            # Limit order
            order = client.create_order(
                symbol=symbol,
                side=side,
                type=Client.ORDER_TYPE_LIMIT,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=f"{price:.2f}"
            )
        else:
            # Market order
            order = client.create_order(
                symbol=symbol,
                side=side,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
        logging.info(f"Order placed: {order}")
        return order
    except Exception as e:
        logging.error(f"Failed to place order: {e}")
        raise

def get_account_balance(client: Client, asset: str):
    """
    Retrieve the balance of a specific asset from Binance.

    Parameters:
    - client: Binance Client object.
    - asset: Asset symbol (e.g., BTC, USDT).

    Returns:
    - Balance available for the specified asset.
    """
    try:
        account = client.get_account()
        for balance in account['balances']:
            if balance['asset'] == asset:
                return float(balance['free'])
        return 0.0
    except Exception as e:
        logging.error(f"Failed to retrieve balance: {e}")
        raise

def check_order_status(client: Client, symbol: str, order_id: str):
    """
    Check the status of an order on Binance.

    Parameters:
    - client: Binance Client object.
    - symbol: Trading pair (e.g., BTCUSDT).
    - order_id: ID of the order to check.

    Returns:
    - Order status response from Binance.
    """
    try:
        order_status = client.get_order(symbol=symbol, orderId=order_id)
        logging.info(f"Order status: {order_status}")
        return order_status
    except Exception as e:
        logging.error(f"Failed to check order status: {e}")
        raise
