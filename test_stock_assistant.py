import requests
import json

def test_stock_assistant():
    print("Testing Stock Market Assistant Endpoints")
    print("=" * 50)
    
    # Test stock stats endpoint
    print("1. Testing stock stats endpoint...")
    try:
        response = requests.get('http://127.0.0.1:5000/get_stock_stats?symbol=AAPL')
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("   Stock Stats:")
            print(f"     Symbol: {data.get('symbol', 'N/A')}")
            print(f"     Name: {data.get('name', 'N/A')}")
            print(f"     Exchange: {data.get('exchange', 'N/A')}")
            print(f"     Price: ${data.get('price', 0.0):.2f}")
            print(f"     Change: {data.get('change', 0.0):.2f} ({data.get('changePercent', 0.0):.2f}%)")
            print(f"     Open: ${data.get('open', 0.0):.2f}")
            print(f"     High: ${data.get('high', 0.0):.2f}")
            print(f"     Low: ${data.get('low', 0.0):.2f}")
            print(f"     Previous Close: ${data.get('previousClose', 0.0):.2f}")
            print(f"     Volume: {data.get('volume', 0):,}")
            print(f"     52W High: ${data.get('yearHigh', 0.0):.2f}")
            print(f"     52W Low: ${data.get('yearLow', 0.0):.2f}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    print("\n" + "-" * 50 + "\n")
    
    # Test chart data endpoint
    print("2. Testing chart data endpoint...")
    try:
        response = requests.get('http://127.0.0.1:5000/get_chart_data?symbol=AAPL&period=1d')
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("   Chart Data:")
            print(f"     Symbol: {data.get('symbol', 'N/A')}")
            if 'data' in data and data['data']:
                print(f"     Data Points: {len(data['data'].get('y', []))}")
                if data['data'].get('y'):
                    print(f"     First Price: ${data['data']['y'][0]:.2f}")
                    print(f"     Last Price: ${data['data']['y'][-1]:.2f}")
            else:
                print("     No chart data available")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")

if __name__ == "__main__":
    test_stock_assistant()