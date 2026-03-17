"""
display.py - Presentation helpers for Project 26: Cryptocurrency Real-Time Tracker
===================================================================================

Formats:
    - Header banner
    - Startup configuration/profile block
    - Ticker table (price, volume, market cap per symbol)
    - Order book snapshot block
    - Alert event log
    - Final run summary report
"""

from typing import Any, Dict, List


def format_header() -> str:
    """Return an ASCII banner for the tracker session.

    Returns:
        str: Header text with decorative separators.

    TODO: Implement styled banner matching the example session output.
    """
    pass


def format_startup_guide(config: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """Format startup configuration and data profile details.

    Parameters:
        config (dict): Tracker configuration from create_tracker_config().
        profile (dict): Startup profile from load_tracker_profile().

    Returns:
        str: Multiline startup guide string covering Configuration and Startup sections.

    TODO: Implement startup section showing symbols, alert rule count,
          poll interval, ticks_to_collect, data source, directories,
          and previously saved tick count.
    """
    pass


def format_ticker_table(ticks: List[Dict[str, Any]], poll_number: int) -> str:
    """Format live ticker data as an aligned table.

    Parameters:
        ticks (list[dict]): Tick records from fetch_ticks().
        poll_number (int): Current poll cycle number for the section header.

    Returns:
        str: Aligned table string with Symbol, Price (USD), 24h Volume,
             and Market Cap columns.

    TODO: Implement aligned column formatting with a section header such as:
          'Fetching live tickers (poll N of M):'.
    """
    pass


def format_order_book(snapshot: Dict[str, Any]) -> str:
    """Format an order book snapshot as a readable block.

    Parameters:
        snapshot (dict): Order book snapshot from fetch_order_book().

    Returns:
        str: Multiline block showing symbol, best bid, best ask, and spread.

    TODO: Implement formatted block matching the example session output.
    """
    pass


def format_alert_events(events: List[Dict[str, Any]]) -> str:
    """Format alert evaluation events as a log table.

    Parameters:
        events (list[dict]): Alert event records from check_alerts().

    Returns:
        str: Multiline log with [TRIGGERED] or [OK] prefix per event, including
             symbol, actual price, and rule description.

    TODO: Implement log formatting matching the example session output.
    """
    pass


def format_run_report(summary: Dict[str, Any]) -> str:
    """Format the final run summary.

    Parameters:
        summary (dict): Run summary from create_run_summary().

    Returns:
        str: Full formatted summary including statistics and artifact paths.

    TODO: Implement report formatting covering Summary and Artifacts saved sections.
    """
    pass

