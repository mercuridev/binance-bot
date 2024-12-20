import os
import logging
import json
from dotenv import load_dotenv
from binance.client import Client
from strategies.rsi_strategy import execute_rsi_strategy
from strategies.macd_strategy import execute_macd_strategy
from strategies.sma_strategy import execute_sma_strategy
from logs.trading_report import log_trade, generate_report
from orders.orders_manager import place_order, get_account_balance

# Load environment variables
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(
    filename='logs/trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load configuration parameters
def load_config():
    """Load bot configuration from config/params.json."""
    try:
        with open('config/params.json', 'r') as file:
            config = json.load(file)
            logging.info("Configuration loaded successfully.")
            return config
    except Exception as e:
        logging.error(f"Failed to load configuration: {e}")
        raise

def execute_strategy(client, config):
    """
    Execute the selected trading strategy.
    """
    try:
        for symbol in config.get('symbols', []):
            if config.get('strategy') == 'RSI':
                logging.info(f"Executing RSI Strategy for {symbol}...")
                execute_rsi_strategy(client, symbol, config)
            elif config.get('strategy') == 'MACD':
                logging.info(f"Executing MACD Strategy for {symbol}...")
                execute_macd_strategy(client, symbol, config)
            elif config.get('strategy') == 'SMA':
                logging.info(f"Executing SMA Strategy for {symbol}...")
                execute_sma_strategy(client, symbol, config)
            else:
                logging.warning("No valid strategy specified in configuration.")
    except Exception as e:
        logging.error(f"Error during strategy execution: {e}")
        raise


def main():
    """
    Main function to initialize and run the trading bot.
    """
    # Initialize Binance client
    client = Client(API_KEY, SECRET_KEY)

    # Load configuration
    config = load_config()

    logging.info("Starting Binance Trading Bot...")

    # Execute the selected strategy
    execute_strategy(client, config)

    # Example: Log a trade (replace with actual logic)
    try:
        log_trade('BUY', 'BTCUSDT', 0.01, 45000, 10000)
    except Exception as e:
        logging.error(f"Failed to log trade: {e}")

    # Generate trading report
    try:
        logging.info("Generating trading report...")
        generate_report()
    except Exception as e:
        logging.error(f"Failed to generate report: {e}")

if __name__ == "__main__":
    main()
