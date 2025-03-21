import requests
import re

def get_exchange_rate(from_currency, to_currency):
    """Fetch the real-time exchange rate from an external API."""
    try:
        url = f"https://www.google.com/finance/quote/{from_currency}-{to_currency}"
        response = requests.get(url)
        response.raise_for_status()
        
        pattern = r'data-last-price="([0-9\.]+)"'
        match = re.search(pattern, response.text)
        
        if match:
            rate = float(match.group(1))
            return rate
        else:
            return None
    except Exception as e:
        print(f"Error fetching exchange rate: {str(e)}")
        return None

def convert_currency(amount, from_currency, to_currency):
    """Convert an amount from one currency to another using the exchange rate."""
    rate = get_exchange_rate(from_currency, to_currency)
    if rate:
        return amount * rate
    return None

def get_supported_currencies():
    """Return a list of supported currencies."""
    return ["USD", "CNY", "EUR", "GBP", "JPY"]  # Extend this list as needed