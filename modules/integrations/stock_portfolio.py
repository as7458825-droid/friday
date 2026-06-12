import json
import os

PORTFOLIO_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "portfolio.json"
)


def _load():
    if os.path.isfile(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE) as f:
            return json.load(f)
    return {"stocks": {}, "crypto": {}}


def _save(data):
    mem = os.path.dirname(PORTFOLIO_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_stock(symbol: str, shares: float) -> str:
    data = _load()
    data["stocks"][symbol.upper()] = data["stocks"].get(symbol.upper(), 0) + shares
    _save(data)
    return f"Added {shares} shares of {symbol.upper()}."


def remove_stock(symbol: str) -> str:
    data = _load()
    if symbol.upper() in data["stocks"]:
        del data["stocks"][symbol.upper()]
        _save(data)
        return f"Removed {symbol.upper()} from portfolio."
    return f"{symbol.upper()} not in portfolio."


def add_crypto(symbol: str, amount: float) -> str:
    data = _load()
    data["crypto"][symbol.upper()] = data["crypto"].get(symbol.upper(), 0) + amount
    _save(data)
    return f"Added {amount} {symbol.upper()}."


def get_portfolio() -> str:
    data = _load()
    if not data["stocks"] and not data["crypto"]:
        return "Portfolio is empty. Add stocks or crypto first."
    try:
        import yfinance as yf
    except ImportError:
        return "yfinance not installed. Run: pip install yfinance"
    lines = []
    total_value = 0
    for sym, shares in data["stocks"].items():
        try:
            ticker = yf.Ticker(sym)
            info = ticker.info
            price = (
                info.get("currentPrice")
                or info.get("regularMarketPrice")
                or info.get("previousClose", 0)
            )
            change = info.get("regularMarketChangePercent", 0)
            value = price * shares
            total_value += value
            lines.append(
                f"{sym}: {shares} shares @ ${price:.2f} ({change:+.2f}%) ${value:.2f}"
            )
        except Exception:
            lines.append(f"{sym}: {shares} shares (price unavailable)")
    for sym, amount in data["crypto"].items():
        try:
            import requests

            resp = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={sym.lower()}&vs_currencies=usd",
                timeout=10,
            )
            price = resp.json().get(sym.lower(), {}).get("usd", 0)
            value = price * amount
            total_value += value
            lines.append(f"{sym.upper()}: {amount} @ ${price:.2f} = ${value:.2f}")
        except Exception:
            lines.append(f"{sym.upper()}: {amount} (price unavailable)")
    if not lines:
        return "Could not fetch prices."
    lines.append(f"Total portfolio value: ${total_value:.2f}")
    return " | ".join(lines)


def get_alert(symbol: str, target: float) -> str:
    data = _load()
    if symbol.upper() in data["stocks"]:
        data.setdefault("alerts", [])
        data["alerts"].append({"symbol": symbol.upper(), "target": target})
        _save(data)
        return f"Alert set for {symbol.upper()} at ${target}."
    return f"Add {symbol.upper()} to portfolio first."


def market_summary() -> str:
    try:
        import yfinance as yf

        indices = {"SPY": "S&P 500", "QQQ": "Nasdaq", "DOW": "Dow Jones"}
        lines = []
        for sym, name in indices.items():
            ticker = yf.Ticker(sym)
            info = ticker.info
            price = info.get("regularMarketPrice", 0)
            change = info.get("regularMarketChangePercent", 0)
            lines.append(f"{name}: {price:.0f} ({change:+.2f}%)")
        return "Market: " + " | ".join(lines)
    except Exception:
        return "Market data unavailable."
