import json
import urllib.request

# Function to fetch the complete list of instruments from Angel Broking’s API
# Returns a Python list of dictionaries containing instrument details
def fetch_instrument_list():
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    # Open the URL, read the raw JSON data, and parse it into Python objects
    return json.loads(urllib.request.urlopen(url).read())

# Function to map instrument tokens to ticker symbols for the NSE equities
# Parameters:
#   instrument_list: list of all instruments fetched from the API
#   tickers: list of ticker symbols you want to track
# Returns:
#   A dictionary mapping token -> ticker symbol
def get_token_map(instrument_list: list, tickers: list) -> dict:
    symbol_map = {}
    # Loop through each ticker you want
    for ticker in tickers:
        # Loop through all instruments in the fetched list
        for inst in instrument_list:
            # Check if the instrument matches:
            # 1. Name matches the ticker
            # 2. Exchange segment is NSE
            # 3. Symbol ends with '-EQ' (equity)
            if inst["name"] == ticker and inst["exch_seg"] == "NSE" and inst["symbol"].endswith("-EQ"):
                # Map the instrument token to the ticker
                symbol_map[inst["token"]] = ticker
    return symbol_map
