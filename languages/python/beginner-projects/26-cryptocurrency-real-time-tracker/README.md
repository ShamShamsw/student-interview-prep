# Beginner Project 26: Cryptocurrency Real-Time Tracker

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** CoinGecko API polling, configurable threshold alert engine, rolling price chart, and tick persistence

---

## Why This Project?

Production crypto dashboards must ingest live market data, normalize it across assets, evaluate user-defined price thresholds in real time, and render rolling charts that update with each new tick.

This project teaches a professional polling pipeline where you can:

- configure a list of coin symbols to track,
- fetch live price, volume, and market cap data from the CoinGecko public API,
- retrieve a simplified order book snapshot for any tracked symbol,
- evaluate configurable threshold alert rules against each incoming tick,
- accumulate a rolling tick history and render an interactive price chart using Plotly,
- print a formatted ticker table, order book view, and alert log to the console,
- and persist tick history and a run summary to disk for later review.

---

## Separate Repository

You can also access this project in a separate repository:

[Cryptocurrency Real-Time Tracker Repository](https://github.com/ShamShamsw/cryptocurrency-real-time-tracker.git)

---

## What You Will Build

You will build a command-line crypto tracker that:

1. Accepts a configurable list of coin symbols (e.g., `bitcoin`, `ethereum`, `solana`).
2. Polls the CoinGecko `/simple/price` endpoint at a configurable interval.
3. Normalizes each response into a typed tick record with price, volume, and market cap.
4. Fetches a simplified order book snapshot showing best bid, best ask, and spread.
5. Evaluates threshold alert rules (above/below a target price) against each tick.
6. Accumulates tick history and builds a rolling Plotly price chart.
7. Prints a formatted ticker table, order book block, and alert event log to the console.
8. Persists tick history and a run summary to disk.

---

## Requirements

- Python 3.11+
- `requests`
- `plotly`
- `pandas`

Install with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
   CRYPTOCURRENCY REAL-TIME TRACKER
======================================================================

Configuration:
   Symbols:           bitcoin, ethereum, solana
   Alert rules:       3 configured
   Poll interval:     30 seconds
   Ticks to collect:  1
   Data source:       CoinGecko (public API)

Startup:
   Data directory:    data/
   Outputs directory: data/outputs/
   Previously saved ticks: 0 records

Fetching live tickers (poll 1 of 1):
   Symbol        Price (USD)    24h Volume       Market Cap
   bitcoin        67,842.30    28,415,920,000   1,336,000,000,000
   ethereum        3,512.18     9,183,440,000     422,000,000,000
   solana            182.44     2,041,670,000      83,000,000,000

Order Book Snapshot: bitcoin
   Best Bid:  67,839.50   Qty: 0.52
   Best Ask:  67,845.00   Qty: 0.31
   Spread:         5.50 USD

Alerts:
   [TRIGGERED]  bitcoin   price=67,842.30  rule=above 60000.00
   [OK]         ethereum  price=3,512.18   rule=below 4000.00
   [OK]         solana    price=182.44     rule=below 200.00

Summary:
   Symbols tracked:    3
   Ticks collected:    3
   Alerts triggered:   1

Artifacts saved:
   Ticks:          data/ticks.json
   Run summary:    data/outputs/run_summary.json
   Price chart:    data/outputs/price_chart.html
```
