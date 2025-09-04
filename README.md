## Overview
market-depth-collector is a Python-based tool designed to capture real-time Level-2 market depth data for NSE stocks using Angel Broking’s SmartAPI. It collects bid/ask prices, trade volume, and other market microstructure metrics, then saves them to CSV for further analysis. This tool is ideal for quantitative researchers, algorithmic traders, and data scientists who want to analyze high-frequency market signals or develop trading strategies.


## Features

Real-time subscription to Level-2 market data using WebSocket

Calculates key metrics for each ticker:

Order Book Imbalance (OBI)

Volume Imbalance

Bid-Ask Spread

Mid-Price

Stores structured data in CSV format for historical analysis

Modular design: separate modules for authentication, data collection, and calculations

TOTP-based authentication for secure access

## Technologies

Python 3.x

Pandas

Angel Broking SmartAPI

pyotp (TOTP authentication)

WebSocket for real-time streaming

## Use Case

Designed for quants, algorithmic traders, and data scientists who want to:

Spoof orders detection engine

Build a trading research pipeline

Backtest trading strategies

Analyze high-frequency market signals
