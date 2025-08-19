import os
from datetime import datetime
from collector.auth import authenticate
from collector.instruments import fetch_instrument_list, get_token_map
from collector.collector import DataCollector

KEY_PATH = r"C:\Users\Ekraj\OneDrive\SmartApi"
os.chdir(KEY_PATH)
API_KEY, CLIENT_CODE, PASSWORD, TOTP_KEY = open("key.txt","r").read().split()[0:4]

FILENAME = f"data/market_data_{datetime.now().strftime('%Y%m%d')}.csv"

# Tickers
TICKERS = ["WIPRO","INFY","RELIANCE"] # Short demo, expand as needed

# Market hours check
from datetime import time as dt_time
MARKET_START = dt_time(9,15)
MARKET_END = dt_time(15,30)
def market_open():
    from datetime import datetime
    now = datetime.now().time()
    return MARKET_START <= now <= MARKET_END

# Authentication
jwt_token, feed_token = authenticate(API_KEY, CLIENT_CODE, PASSWORD, TOTP_KEY)

# Instruments & tokens
instrument_list = fetch_instrument_list()
symbol_map = get_token_map(instrument_list, TICKERS)
tokens = list(symbol_map.keys())

# Run Collector
collector = DataCollector(jwt_token, API_KEY, CLIENT_CODE, feed_token, tokens, symbol_map, FILENAME)
collector.run(market_open)

try:
    while True:
        print(f"🟢 {datetime.now().strftime('%H:%M:%S')} | Collector running...")
        time.sleep(10)
except KeyboardInterrupt:
    print("🛑 Manual exit triggered.")
