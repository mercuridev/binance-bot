import os
import logging
import json
from dotenv import load_dotenv
from binance.client import Client
from strategies.rsi_strategy import execute_rsi_strategy
from strategies.macd_strategy import execute_macd_strategy
from trading_report import log_trade, generate_report

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

def main():
    """
    Main function to initialize and run the trading bot.
    """
    # Initialize Binance client
    client = Client(API_KEY, SECRET_KEY)

    # Load configuration
    config = load_config()

    logging.info("Starting Binance Trading Bot...")

    # Select strategy based on config
    try:
        if config.get('strategy') == 'RSI':
            logging.info("Executing RSI Strategy...")
            execute_rsi_strategy(client, config)
        elif config.get('strategy') == 'MACD':
            logging.info("Executing MACD Strategy...")
            execute_macd_strategy(client, config)
        else:
            logging.warning("No valid strategy specified in configuration.")

        # Example of logging a trade (to be replaced with actual trade logic)
        log_trade('BUY', 'BTCUSDT', 0.01, 45000, 10000)

        # Generate trading report
        logging.info("Generating trading report...")
        generate_report()

    except Exception as e:
        logging.error(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
