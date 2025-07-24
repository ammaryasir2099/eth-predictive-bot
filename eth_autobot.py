import time
import logging
import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ----------------------------- #
# ?? Load environment variables
# ----------------------------- #
def load_api_keys():
    dotenv_paths = [".env", "r.env"]
    loaded = False
    for path in dotenv_paths:
        if os.path.exists(path):
            load_dotenv(dotenv_path=path)
            loaded = True
            break

    if not loaded:
        logging.warning("No .env file found. Falling back to manual input.")
    
    api_key = os.getenv("BINANCE_API_KEY") or input("Enter your Binance API KEY: ").strip()
    api_secret = os.getenv("BINANCE_API_SECRET") or input("Enter your Binance API SECRET: ").strip()

    if not api_key or not api_secret:
        raise ValueError("? Binance API Key/Secret missing. Check your .env file or inputs.")

    return api_key, api_secret

# ----------------------------- #
# ?? Bot Configuration
# ----------------------------- #
symbol = "ETHUSDT"
base_investment = 5.0  # USDT
leverage = 11
step_size = 1.0  # ETH price step

# Dynamic precision (fetched from exchange)
quantity_precision = 1
tick_size = 0.01

progression_factor = 1.1  # Geometric increase
buy_step_count = 0
sell_step_count = 0

# ----------------------------- #
# ?? Binance Setup
# ----------------------------- #
def setup_client():
    api_key, api_secret = load_api_keys()
    client = Client(api_key, api_secret)
    try:
        client.futures_account()
    except BinanceAPIException as e:
        logging.error(f"? Binance auth failed: {e}")
        raise
    return client

# ----------------------------- #
# ?? Fetch Precision from Binance
# ----------------------------- #
def get_symbol_info(client):
    global quantity_precision, tick_size
    try:
        exchange_info = client.futures_exchange_info()
        symbol_info = next(s for s in exchange_info['symbols'] if s['symbol'] == symbol)
        quantity_precision = int(symbol_info['quantityPrecision'])
        tick_size = float(next(f for f in symbol_info['filters'] if f['filterType'] == 'PRICE_FILTER')['tickSize'])
        logging.info(f"? Symbol loaded: Precision = {quantity_precision}, Tick size = {tick_size}")
    except Exception as e:
        logging.error(f"? Could not fetch symbol info: {e}")
        raise

def round_price(price):
    return round(price / tick_size) * tick_size

def round_quantity(quantity):
    return round(quantity, quantity_precision)

def calculate_quantity(usdt, price):
    return round_quantity(usdt / price)

def fetch_current_price(client):
    ticker = client.futures_mark_price(symbol=symbol)
    return float(ticker['markPrice'])

def calculate_next_investment(base, step_count):
    return base * (progression_factor ** step_count)

def next_buy_price(last_price, step_count):
    return round_price(last_price - step_size * (step_count * 2 - 1))

def next_sell_price(last_price, step_count):
    return round_price(last_price + step_size * (step_count * 2 - 1))

def place_market_order(client, side, quantity):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
        logging.info(f"{side} MARKET order placed: Qty {quantity}")
        return order
    except BinanceAPIException as e:
        logging.error(f"Failed to place {side} MARKET order: {e}")
        return None

def place_limit_order(client, side, price, quantity):
    price = round_price(price)
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            price=price,
            quantity=quantity,
            timeInForce="GTC"
        )
        logging.info(f"{side} LIMIT order at {price} for {quantity}")
        return order
    except BinanceAPIException as e:
        logging.error(f"Failed to place {side} LIMIT order: {e}")
        return None

def place_initial_orders(client):
    global buy_step_count, sell_step_count
    current_price = fetch_current_price(client)

    buy_quantity = calculate_quantity(base_investment, current_price)
    place_market_order(client, "BUY", buy_quantity)

    sell_quantity = calculate_quantity(base_investment, current_price)
    place_market_order(client, "SELL", sell_quantity)

    buy_step_count = 1
    sell_step_count = 1
    logging.info(f"?? Initial orders placed at {current_price}")

# ----------------------------- #
# ?? Main Trading Loop
# ----------------------------- #
def trading_loop():
    global buy_step_count, sell_step_count

    client = setup_client()
    get_symbol_info(client)
    place_initial_orders(client)

    last_buy_price = fetch_current_price(client)
    last_sell_price = last_buy_price

    while True:
        try:
            current_price = fetch_current_price(client)

            if current_price <= next_buy_price(last_buy_price, buy_step_count):
                invest = calculate_next_investment(base_investment, buy_step_count)
                quantity = calculate_quantity(invest, current_price)
                place_limit_order(client, "BUY", current_price, quantity)
                logging.info(f"? Buy Step {buy_step_count}: {invest:.2f} USDT at {current_price}")
                last_buy_price = current_price
                buy_step_count += 1

            if current_price >= next_sell_price(last_sell_price, sell_step_count):
                invest = calculate_next_investment(base_investment, sell_step_count)
                quantity = calculate_quantity(invest, current_price)
                place_limit_order(client, "SELL", current_price, quantity)
                logging.info(f"? Sell Step {sell_step_count}: {invest:.2f} USDT at {current_price}")
                last_sell_price = current_price
                sell_step_count += 1

            time.sleep(1)

        except KeyboardInterrupt:
            logging.warning("?? Bot manually stopped.")
            break
        except Exception as e:
            logging.error(f"?? Error in loop: {e}")
            time.sleep(5)

# ----------------------------- #
# ?? Entry Point
# ----------------------------- #
if __name__ == "__main__":
    try:
        trading_loop()
    except Exception as e:
        logging.critical(f"?? Bot crashed: {e}")
