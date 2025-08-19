# Level 2 Market Data Collector

## Overview
This project collects **real-time Level 2 market data** (order book and trades) from the NSE using Angel Broking SmartAPI.  
It computes key microstructure metrics such as:
- Order Book Imbalance (OBI)
- Volume Imbalance
- Spread
- Mid Price  

Data is saved to CSV for further quantitative analysis, modeling, or backtesting.

---

## Features
- Real-time WebSocket data collection
- Thread-safe order book and trade handling
- Automatic CSV logging every 30 records
- Modular design for easy extension
- Configurable ticker list

---

## Installation
1. Clone this repository:
```bash
git clone https://github.com/yourusername/level2_market_collector.git
cd level2_market_collector

2. pip install -r requirements.txt

3.API_KEY CLIENT_CODE PASSWORD TOTP_KEY

4.python main.py




