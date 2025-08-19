import threading
import time
from datetime import datetime
import pandas as pd
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from collector import calculations  # your helper functions for OBI, volume imbalance, spread

# === DataCollector Class ===
# This class handles real-time Level 2 market data collection via WebSocket
# It collects order book snapshots, calculates metrics, and saves to CSV
class DataCollector:
    
    # Constructor: initializes the WebSocket, state variables, and threading lock
    def __init__(self, jwt_token, api_key, client_code, feed_token, tokens, symbol_map, filename):
        self.tokens = tokens                    # list of instrument tokens to subscribe
        self.symbol_map = symbol_map            # token -> ticker mapping
        self.order_books = {}                   # stores latest bid/ask book for each symbol
        self.trades = {}                        # stores recent trades for each symbol
        self.data = []                          # buffer for calculated metrics to be saved
        self.lock = threading.Lock()            # ensures thread-safe access to shared data
        self.filename = filename                # CSV filename for storing collected data

        # Initialize the SmartWebSocketV2 client
        self.ws = SmartWebSocketV2(jwt_token, api_key, client_code, feed_token)
        self.ws.on_open = self.on_open
        self.ws.on_data = self.on_data
        self.ws.on_error = self.on_error

    # Callback when WebSocket opens
    def on_open(self, ws):
        print("✅ WebSocket connected.")
        # Subscribe to Level 2 data for all tokens
        self.ws.subscribe("stream_1", 3, [{"exchangeType":1, "tokens":self.tokens}])

    # Callback when new data is received from WebSocket
    def on_data(self, ws, msg):
        # Ensure msg is a Python dict
        msg = msg if isinstance(msg, dict) else json.loads(msg)
        token = msg.get("token")
        symbol = self.symbol_map.get(token, "UNKNOWN")
        if symbol == "UNKNOWN":                # ignore unrecognized tokens
            return
        
        # Extract bid/ask data
        bid = [(float(b["price"]), int(b["quantity"])) for b in msg.get("best_5_buy_data",[])]
        ask = [(float(a["price"]), int(a["quantity"])) for a in msg.get("best_5_sell_data",[])]
        ltq = int(msg.get("ltq", 0))          # last traded quantity
        side = msg.get("c", "B")              # trade side (B/S)

        # Thread-safe update of order_books and trades
        with self.lock:
            self.order_books[symbol] = {"bid":bid, "ask":ask}
            self.trades.setdefault(symbol, []).append({"volume":ltq, "type":"buy" if side=="B" else "sell"})

    # Callback when WebSocket encounters an error
    def on_error(self, ws, err):
        print("❌ WebSocket error:", err)

    # Main loop for collecting metrics while market is open
    def collect_loop(self, market_open_func):
        while market_open_func():  # continue while market is open
            with self.lock:
                for symbol, book in self.order_books.items():
                    trades = self.trades.get(symbol, [])
                    if not book["bid"] or not book["ask"]:  # skip if incomplete order book
                        continue

                    # Calculate metrics using helper functions
                    obi = calculations.calculate_obi(book["bid"], book["ask"])
                    vol_imb = calculations.calculate_vol_imbalance(trades)
                    spread = calculations.calculate_spread(book["bid"], book["ask"])
                    mid_price = (book["bid"][0][0] + book["ask"][0][0])/2

                    # Append metrics to data buffer
                    self.data.append({
                        "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "symbol":symbol,
                        "obi":obi,
                        "volume_imbalance":vol_imb,
                        "spread":spread,
                        "mid_price":mid_price
                    })

                # Save to CSV every 30 records
                if len(self.data) >= 30:
                    pd.DataFrame(self.data).to_csv(
                        self.filename,
                        mode='a',
                        header=not pd.io.common.file_exists(self.filename),
                        index=False
                    )
                    self.data = []  # reset buffer
            time.sleep(1)  # avoid busy waiting

    # Run method to start collection in a separate thread and connect WebSocket
    def run(self, market_open_func):
        threading.Thread(target=self.collect_loop, args=(market_open_func,), daemon=True).start()
        self.ws.connect()
