import json
import urllib.request

def fetch_instrument_list():
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    return json.loads(urllib.request.urlopen(url).read())

def get_token_map(instrument_list: list, tickers: list) -> dict:
    symbol_map = {}
    for ticker in tickers:
        for inst in instrument_list:
            if inst["name"] == ticker and inst["exch_seg"] == "NSE" and inst["symbol"].endswith("-EQ"):
                symbol_map[inst["token"]] = ticker
    return symbol_map
