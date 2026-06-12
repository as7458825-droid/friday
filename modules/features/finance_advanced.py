def nifty_status() -> str:
    try:
        import requests

        r = requests.get(
            "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=5,
        )
        data = r.json()
        last = data["data"][0]["lastPrice"]
        change = data["data"][0]["change"]
        return f"Nifty 50: {last} ({change:+.2f})"
    except Exception:
        return "Could not fetch Nifty data."


def mutual_fund_schemes() -> str:
    return "Top funds:\n- Parag Parikh Flexi Cap\n- HDFC Balanced Advantage\n- SBI Small Cap\n- ICICI Bluechip\nCheck: https://www.valueresearchonline.com/"


def gold_price() -> str:
    try:
        import requests

        r = requests.get(
            "https://www.goldapi.io/api/XAU/INR",
            headers={"x-access-token": os.environ.get("GOLD_API_KEY", "")},
            timeout=5,
        )
        data = r.json()
        return f"Gold: ₹{data['price']}/oz"
    except Exception:
        return "Gold price unavailable. Try: https://www.goodreturns.in/gold-rates/"


import os


def crypto_all() -> str:
    try:
        import requests

        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,ripple,dogecoin&vs_currencies=inr",
            timeout=5,
        )
        data = r.json()
        return " | ".join(f"{c}: ₹{v['inr']}" for c, v in data.items())
    except Exception:
        return "Crypto data unavailable."
