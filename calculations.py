def calculate_obi(bid: list, ask: list) -> float:
    bq = sum(q for _, q in bid)
    aq = sum(q for _, q in ask)
    return round((bq - aq) / (bq + aq), 4) if bq + aq != 0 else 0

def calculate_vol_imbalance(trades: list) -> float:
    buy = sum(t["volume"] for t in trades if t["type"] == "buy")
    sell = sum(t["volume"] for t in trades if t["type"] == "sell")
    return round((buy - sell) / (buy + sell), 4) if buy + sell != 0 else 0

def calculate_spread(bid: list, ask: list) -> float:
    return round(ask[0][0] - bid[0][0], 4) if bid and ask else 0
