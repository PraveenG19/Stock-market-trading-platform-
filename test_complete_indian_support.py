"""
Comprehensive test for Indian stock market support
"""
import requests
import json

def test_complete_indian_support():
    """
    Test all Indian stock market functionality
    """
    print("Testing Complete Indian Stock Market Support")
    print("=" * 60)
    
    # Test 1: Angel One Data API for Indian stocks
    print("\n1. Testing Angel One Data API for Indian Stocks")
    print("-" * 50)
    
    indian_stocks = [
        "RELIANCE.NS",
        "TCS.NS", 
        "INFY.NS"
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
                    print(f"    Currency: {data['currency_symbol']}")
            else:
                print(f"  ❌ HTTP Error: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Exception: {e}")
    
    # Test 2: Regular stock data API for Indian stocks
    print("\n\n2. Testing Regular Stock Data API for Indian Stocks")
    print("-" * 50)
    
    for symbol in indian_stocks:
        print(f"\nTesting {symbol}...")
        try:
            response = requests.get(f'http://127.0.0.1:5000/get_stock_data?symbol={symbol}')
            if response.status_code == 200:
                data = response.json()
                if 'error' in data:
                    print(f"  ❌ Error: {data['error']}")
                else:
                    print(f"  ✅ Success:")
                    print(f"    Symbol: {data['symbol']}")
                    print(f"    Price: ₹{data['price']:.2f}")
                    print(f"    Change: {data['change']:.2f} ({data['changePercent']:.2f}%)")
                    print(f"    Name: {data['name']}")
            else:
                print(f"  ❌ HTTP Error: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Exception: {e}")
    
    # Test 3: Prediction Chart for Indian stocks
    print("\n\n3. Testing Prediction Chart for Indian Stocks")
    print("-" * 50)
    
    symbol = "RELIANCE.NS"
    print(f"\nTesting prediction chart for {symbol}...")
    try:
        response = requests.get(f'http://127.0.0.1:5000/prediction_chart/{symbol}')
        if response.status_code == 200:
            print(f"  ✅ Success: Prediction chart page loaded")
            # Check if the response contains the right currency symbol
            if '₹' in response.text:
                print(f"  ✅ Indian Rupee symbol (₹) found in response")
            else:
                print(f"  ⚠️  Indian Rupee symbol (₹) not found in response")
        else:
            print(f"  ❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Exception: {e}")
    
    # Test 4: Compare with US stocks
    print("\n\n4. Comparing with US Stocks")
    print("-" * 50)
    
    us_stock = "AAPL"
    print(f"\nTesting US stock {us_stock} for comparison...")
    try:
        response = requests.get(f'http://127.0.0.1:5000/get_angelone_data?symbol={us_stock}&period=1d')
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
                print(f"    Currency: {data['currency_symbol']}")
        else:
            print(f"  ❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Exception: {e}")
    
    print("\n" + "=" * 60)
    print("Testing complete! Check the results above.")

if __name__ == "__main__":
    test_complete_indian_support()