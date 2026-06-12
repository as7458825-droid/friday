import yfinance as yf
import ccxt
import logging

log = logging.getLogger("FRIDAY.Finance")


def get_stock_price(ticker: str) -> str:
    """Fetch real-time stock price and trend."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        current = info.get("regularMarketPrice") or info.get("currentPrice")
        currency = info.get("currency", "USD")

        if current is None:
            return f"Could not find price for {ticker}."

        change = info.get("regularMarketChangePercent", 0)
        trend = "▲" if change > 0 else "▼"
        return f"{ticker}: {current} {currency} ({trend} {change:.2f}%)"
    except Exception as e:
        log.error(f"Stock Fetch Error: {e}")
        return f"Error fetching stock {ticker}: {e}"


def get_crypto_price(symbol: str) -> str:
    """Fetch real-time crypto price from Binance."""
    try:
        exchange = ccxt.binance()
        ticker = exchange.fetch_ticker(f"{symbol.upper()}/USDT")
        last = ticker["last"]
        change = ticker["percentage"]
        trend = "▲" if change > 0 else "▼"
        return f"{symbol.upper()}: ${last} ({trend} {change:.2f}%)"
    except Exception as e:
        log.error(f"Crypto Fetch Error: {e}")
        return f"Error fetching crypto {symbol}: {e}"


def get_market_summary() -> str:
    """Get a quick summary of major indices."""
    indices = {"S&P 500": "^GSPC", "Nasdaq": "^IXIC", "Bitcoin": "BTC-USD"}
    summary = []
    for name, ticker in indices.items():
        try:
            t = yf.Ticker(ticker)
            price = t.info.get("regularMarketPrice") or t.info.get("currentPrice")
            summary.append(f"{name}: {price}")
        except Exception:
            continue
    return " | ".join(summary)
