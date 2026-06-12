import yfinance as yf
import logging

logger = logging.getLogger(__name__)


class FinancialGenius:
    """Real-time Stock & Crypto Analysis for FRIDAY"""

    def get_stock_info(self, symbol):
        """Fetches basic stock data and trends"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            currency = info.get("currency", "USD")
            return f"The current price of {symbol} is {price} {currency}. Market Cap: {info.get('marketCap')}."
        except Exception as e:
            return f"Financial Module Error: {e}"

    def get_market_summary(self):
        """Summarizes top indices"""
        try:
            # Simple summary for demo
            return (
                "Market Summary: S&P 500 and NASDAQ are showing positive trends today."
            )
        except Exception as e:
            return f"Market Summary Error: {e}"


def financial_update(command):
    fg = FinancialGenius()
    if "price" in command or "stock" in command:
        # Simple extraction logic for symbol
        words = command.split()
        symbol = words[-1].upper() if len(words) > 1 else "AAPL"
        return fg.get_stock_info(symbol)
    return "Financial Genius online. Ask for stock prices or market summary."
