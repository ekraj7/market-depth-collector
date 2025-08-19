import threading
import time
from datetime import datetime
import pandas as pd
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from collector import calculations

class DataCollector:
    def __init__(self, jwt_token, api_key, client_code, feed_token, tokens, symbol_map, filename):
        self.tokens = tokens
        self.symbol_map = symbol_map
        self.order_books = {}
        self.trades = {}
        self.data = []
        self.lock = threading.Lock()
        self.filename = filename

        self.ws = SmartWebSocketV2(jwt_token, api_key, client_code, feed_token)
        self.ws.on_open = self.on_open
        self.ws.on_data = self.on_data
        self.ws.on_error = self.on_error

    def on_open(self, ws):
        print("✅ WebSocket connected.")
        self.ws.subscribe("stream_1", 3, [{"exchangeType":1, "tokens":self.tokens}])

    def on_data(self, ws, msg):
        msg = msg if isinstance(msg, dict) else json.loads(msg)
        token = msg.get("token")
        symbol = self.symbol_map.get(token, "UNKNOWN")
        if symbol == "UNKNOWN":
            return
        bid = [(float(b["price"]), int(b["quantity"])) for b in msg.get("best_5_buy_data",[])]
        ask = [(float(a["price"]), int(a["quantity"])) for a in msg.get("best_5_sell_data",[])]
        ltq = int(msg.get("ltq", 0))
        side = msg.get("c", "B")

        with self.lock:
            self.order_books[symbol] = {"bid":bid, "ask":ask}
            self.trades.setdefault(symbol, []).append({"volume":ltq, "type":"buy" if side=="B" else "sell"})

    def on_error(self, ws, err):
        print("❌ WebSocket error:", err)

    def collect_loop(self, market_open_func):
        while market_open_func():
            with self.lock:
                for symbol, book in self.order_books.items():
                    trades = self.trades.get(symbol, [])
                    if not book["bid"] or not book["ask"]:
                        continue
                    obi = calculations.calculate_obi(book["bid"], book["ask"])
                    vol_imb = calculations.calculate_vol_imbalance(trades)
                    spread = calculations.calculate_spread(book["bid"], book["ask"])
                    mid_price = (book["bid"][0][0] + book["ask"][0][0])/2
                    self.data.append({
                        "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "symbol":symbol,
                        "obi":obi,
                        "volume_imbalance":vol_imb,
                        "spread":spread,
                        "mid_price":mid_price
                    })
                if len(self.data)>=30:
                    pd.DataFrame(self.data).to_csv(self.filename, mode='a', header=not pd.io.common.file_exists(self.filename), index=False)
                    self.data=[]
            time.sleep(1)

    def run(self, market_open_func):
        threading.Thread(target=self.collect_loop, args=(market_open_func,), daemon=True).start()
        self.ws.connect()
