import os
import pandas as pd
import matplotlib.pyplot as plt

# Ensure the reports directory exists
if not os.path.exists('logs/reports'):
    os.makedirs('logs/reports')

def log_trade(action, symbol, quantity, price, balance):
    """
    Logs a trade to a CSV file.

    Parameters:
    - action: 'BUY' or 'SELL'.
    - symbol: Trading pair (e.g., BTCUSDT).
    - quantity: Quantity traded.
    - price: Price of the trade.
    - balance: Current balance after the trade.
    """
    log_file = 'logs/reports/trading_log.csv'
    columns = ['action', 'symbol', 'quantity', 'price', 'balance', 'timestamp']

    # Create log file if it doesn't exist
    if not os.path.exists(log_file):
        df = pd.DataFrame(columns=columns)
        df.to_csv(log_file, index=False)

    # Append trade to log
    df = pd.read_csv(log_file)
    df = pd.concat([
        df,
        pd.DataFrame({
            'action': [action],
            'symbol': [symbol],
            'quantity': [quantity],
            'price': [price],
            'balance': [balance],
            'timestamp': [pd.Timestamp.now()]
        })
    ])
    df.to_csv(log_file, index=False)

def generate_report():
    """
    Generate a trading report with statistics and a balance chart.
    """
    log_file = 'logs/reports/trading_log.csv'
    if not os.path.exists(log_file):
        print("No trading log found to generate a report.")
        return

    df = pd.read_csv(log_file)

    # Summary statistics
    total_trades = len(df)
    total_buys = len(df[df['action'] == 'BUY'])
    total_sells = len(df[df['action'] == 'SELL'])
    avg_buy_price = df[df['action'] == 'BUY']['price'].mean() if total_buys > 0 else 0
    avg_sell_price = df[df['action'] == 'SELL']['price'].mean() if total_sells > 0 else 0

    print("Trading Report")
    print("===============")
    print(f"Total Trades: {total_trades}")
    print(f"Total Buys: {total_buys}")
    print(f"Total Sells: {total_sells}")
    print(f"Average Buy Price: {avg_buy_price:.2f}")
    print(f"Average Sell Price: {avg_sell_price:.2f}")

    # Plot balance over time
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df['balance'], marker='o', label='Balance')
    plt.title('Account Balance Over Time')
    plt.xlabel('Time')
    plt.ylabel('Balance')
    plt.legend()
    plt.grid()
    plt.savefig('logs/reports/balance_chart.png')
    plt.show()

# Example usage
if __name__ == "__main__":
    log_trade('BUY', 'BTCUSDT', 0.01, 45000, 10000)
    log_trade('SELL', 'BTCUSDT', 0.005, 48000, 10500)
    generate_report()
