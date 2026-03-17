"""
models.py - Data models for Project 26: Cryptocurrency Real-Time Tracker
=========================================================================

Defines:
    - Tracker configuration (symbols, alert rules, poll interval, data source)
    - Tick records (price, volume, market cap per symbol per poll)
    - Order book snapshot records (best bid, best ask, spread)
    - Alert event records (symbol, rule type, threshold, actual value)
    - Final run summary record for reporting and persistence
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string.

    Returns:
        str: UTC timestamp with trailing Z.
    """
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def create_tracker_config(
    symbols: Optional[List[str]] = None,
    alert_rules: Optional[List[Dict[str, Any]]] = None,
    poll_interval: int = 30,
    ticks_to_collect: int = 1,
    data_source: str = "CoinGecko (public API)",
) -> Dict[str, Any]:
    """Create a default tracker configuration record.

    Parameters:
        symbols (list[str] | None): Coin IDs to track (e.g., 'bitcoin', 'ethereum').
                                    Defaults to ['bitcoin', 'ethereum', 'solana'].
        alert_rules (list[dict] | None): Alert rule dicts with keys 'symbol',
                                         'condition' ('above'|'below'), and 'threshold'.
                                         Defaults to three example rules.
        poll_interval (int): Seconds between each price poll.
        ticks_to_collect (int): Total number of poll cycles to run before exiting.
        data_source (str): Human-readable label for the data source.

    Returns:
        dict: Configuration dictionary used throughout the tracker pipeline.

    TODO: Implement configuration creation with default values.
          Use default symbols and default alert_rules when callers pass None.
    """
    pass


def create_tick(
    symbol: str,
    price_usd: float,
    volume_24h: float,
    market_cap: float,
) -> Dict[str, Any]:
    """Create a normalized price tick record for one symbol.

    Parameters:
        symbol (str): Coin identifier (e.g., 'bitcoin').
        price_usd (float): Current price in USD.
        volume_24h (float): 24-hour trading volume in USD.
        market_cap (float): Market capitalization in USD.

    Returns:
        dict: Tick record including a UTC fetched_at timestamp.

    TODO: Implement tick record creation with a fetched_at timestamp from _utc_timestamp().
    """
    pass


def create_order_book_snapshot(
    symbol: str,
    best_bid: float,
    best_bid_qty: float,
    best_ask: float,
    best_ask_qty: float,
) -> Dict[str, Any]:
    """Create an order book snapshot record for one symbol.

    Parameters:
        symbol (str): Coin identifier.
        best_bid (float): Highest buy price in the order book.
        best_bid_qty (float): Quantity available at the best bid.
        best_ask (float): Lowest sell price in the order book.
        best_ask_qty (float): Quantity available at the best ask.

    Returns:
        dict: Snapshot record including derived spread and a UTC timestamp.

    Derived field:
        spread = best_ask - best_bid

    TODO: Implement snapshot creation with computed spread and fetched_at timestamp.
    """
    pass


def create_alert_event(
    symbol: str,
    condition: str,
    threshold: float,
    actual_value: float,
    triggered: bool,
) -> Dict[str, Any]:
    """Create an alert evaluation event record.

    Parameters:
        symbol (str): Coin identifier the alert applies to.
        condition (str): Alert condition type ('above' or 'below').
        threshold (float): The price level that triggers the alert.
        actual_value (float): The current price observed during evaluation.
        triggered (bool): True if the alert condition was met.

    Returns:
        dict: Alert event record including a UTC evaluated_at timestamp.

    TODO: Implement alert event creation with evaluated_at timestamp.
    """
    pass


def create_run_summary(
    config: Dict[str, Any],
    ticks_collected: int,
    alerts_triggered: int,
    symbols_tracked: int,
    artifacts: Dict[str, str],
) -> Dict[str, Any]:
    """Create the final run summary record.

    Parameters:
        config (dict): Tracker configuration snapshot.
        ticks_collected (int): Total tick records gathered across all polls.
        alerts_triggered (int): Number of alert events that fired as triggered.
        symbols_tracked (int): Number of distinct symbols watched.
        artifacts (dict): Saved output paths (ticks JSON, summary JSON, chart HTML).

    Returns:
        dict: Complete run summary for display and persistence including a
              UTC completed_at timestamp.

    TODO: Implement summary creation with timestamp from _utc_timestamp().
    """
    pass

