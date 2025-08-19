# Level 2 Market Data Collector

## Overview
Level-2 Data Collector is a Python-based tool designed to fetch and store real-time market depth data for selected NSE stocks using Angel Broking’s SmartAPI. The project focuses on capturing high-frequency trading information, including order book data, volume imbalances, spreads, and mid-prices, which can be used for quantitative research, algorithmic trading strategies, and market analysis.

Key Features:

Real-time subscription to Level-2 market data via WebSocket.

Fetches bid/ask data for multiple tickers and calculates key metrics:

Order Book Imbalance (OBI)

Volume Imbalance

Bid-Ask Spread

Mid-Price

Saves structured data to CSV files for historical analysis.

Modular design with separate components for authentication, data collection, and calculations.

Safe handling of credentials with TOTP-based authentication.

Technologies Used:

Python 3.x

Pandas

Angel Broking SmartAPI

pyotp (for TOTP authentication)

WebSocket for real-time data streaming

Use Case:
This project is suitable for aspiring quants, algo traders, and data scientists looking to build a trading research pipeline, backtest strategies, or analyze high-frequency market signals.


