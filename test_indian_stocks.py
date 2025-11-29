"""
Test script for Indian stock market functionality
"""
import requests
import json

def test_indian_stocks():
    """
    Test Indian stock market data fetching
    """
    print("Testing Indian Stock Market Functionality")
    print("=" * 50)
    
    # Test Indian stocks
    indian_stocks = [
        "RELIANCE.NS",
        "TCS.NS", 
        "INFY.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS"
    ]
    
    for symbol in indian_stocks:
        print(f"\nTesting {symbol}...")
        try:
            response = requests.get(f'http://127.0.0.1:5000/get_angelone_data?symbol={symbol}&period=1d')
            if response.status_code == 200:
                data = response.json()
                if 'error' in data:
                    print(f"  ❌ Error: {data['error']}")
                else:
                    print(f"  ✅ Success:")
                    print(f"    Symbol: {data['symbol']}")
                    print(f"    Exchange: {data['exchange']}")
                    print(f"    LTP: {data['currency_symbol']}{data['ltp']:.2f}")
                    print(f"    Change: {data['change_abs']:.2f} ({data['change_pct']:.2f}%)")
            else:
                print(f"  ❌ HTTP Error: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Exception: {e}")
    
    # Test US stocks for comparison
    print("\n\nTesting US Stocks for Comparison")
    print("=" * 50)
    
    us_stocks = ["AAPL", "MSFT", "GOOGL"]
    
    for symbol in us_stocks:
        print(f"\nTesting {symbol}...")
        try:
            response = requests.get(f'http://127.0.0.1:5000/get_angelone_data?symbol={symbol}&period=1d')
            if response.status_code == 200:
                data = response.json()
                if 'error' in data:
                    print(f"  ❌ Error: {data['error']}")
                else:
                    print(f"  ✅ Success:")
                    print(f"    Symbol: {data['symbol']}")
                    print(f"    Exchange: {data['exchange']}")
                    print(f"    LTP: {data['currency_symbol']}{data['ltp']:.2f}")
                    print(f"    Change: {data['change_abs']:.2f} ({data['change_pct']:.2f}%)")
            else:
                print(f"  ❌ HTTP Error: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Exception: {e}")

if __name__ == "__main__":
    test_indian_stocks()