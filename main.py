# === Import Required Libraries ===
import os
import time
from datetime import datetime, time as dt_time
from collector.auth import authenticate               # Handles login/authentication with SmartAPI
from collector.instruments import fetch_instrument_list, get_token_map  # Fetch & map instruments
from collector.collector import DataCollector         # Custom data collector class
from pyotp import TOTP                                # For generating OTP (2FA)

# === Setup File Paths & Load Credentials ===
KEY_PATH = r"C:\Users\Ekraj\OneDrive\Projects\Tokens"   # Path where your key.txt is stored
os.chdir(KEY_PATH)                                      # Change working directory to Tokens folder

# Read credentials from key.txt (manual indexing to match your file structure)
key_secret = open("key.txt", "r").read().split()
API_KEY    = key_secret[0]   # API key
CLIENT_CODE = key_secret[2]  # Client code
PASSWORD   = key_secret[3]   # Password
TOTP_KEY   = key_secret[4]   # Base32 TOTP secret (Google Authenticator)

# === Setup Output File ===
FILENAME = f"data/market_data_{datetime.now().strftime('%Y%m%d')}.csv"
# Example: data/market_data_20250824.csv

# === Define Market Hours ===
MARKET_START = dt_time(9, 15)   # Market opens at 9:15 AM
MARKET_END   = dt_time(15, 30)  # Market closes at 3:30 PM

def market_open():
    """Check if current time is within market hours."""
    now = datetime.now().time()
    return MARKET_START <= now <= MARKET_END

# === Authenticate with SmartAPI ===
print("🚀 Authenticating...")
jwt_token, feed_token = authenticate(API_KEY, CLIENT_CODE, PASSWORD, TOTP_KEY)
print("✅ Authentication successful")

# === Fetch Instrument List & Map Symbols to Tokens ===
instrument_list = fetch_instrument_list()                           # Get list of all tradable instruments
symbol_map = get_token_map(instrument_list, ["WIPRO","INFY","RELIANCE"])  
# Create mapping between symbol → token (for selected tickers)
tokens = list(symbol_map.keys())                                    # Extract only tokens

# === Initialize Collector ===
collector = DataCollector(jwt_token, API_KEY, CLIENT_CODE, feed_token, tokens, symbol_map, FILENAME)
collector.run(market_open)   # Start WebSocket & data collection

# === Keep Collector Running Until Market Close ===
# === Keep Collector Running Until Market Close ===
try:
    while True:
        if not market_open():
            # If market is closed → exit gracefully
            print("🔒 Market closed. Shutting down gracefully...")
            collector.ws.disconnect()   # ✅ Proper way to close SmartWebSocketV2
            break
        # Otherwise → keep running
        print(f"🟢 {datetime.now().strftime('%H:%M:%S')} | Collector running...")
        time.sleep(10)   # Sleep for 10 seconds before checking again

# === Manual Exit Handling ===
except KeyboardInterrupt:
    print("🛑 Manual exit triggered.")
    collector.ws.disconnect()   # ✅ Close WebSocket when user presses Ctrl+C


# === Debug: Print OTP ===
totp = TOTP(TOTP_KEY.replace(" ", "").upper())  # Clean secret (spaces removed, uppercase)
print("Generated OTP:", totp.now())             # Print OTP for testing
