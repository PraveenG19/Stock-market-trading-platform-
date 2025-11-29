import requests
import json

# Test stock data endpoint
print("Testing stock data endpoint...")
try:
    response = requests.get('http://127.0.0.1:5000/get_stock_data?symbol=AAPL')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Stock Data:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")

print("\n" + "="*50 + "\n")

# Test chart data endpoint
print("Testing chart data endpoint...")
try:
    response = requests.get('http://127.0.0.1:5000/get_chart_data?symbol=AAPL&period=1mo')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Chart Data:")
        print(f"Symbol: {data.get('symbol', 'N/A')}")
        if 'data' in data and data['data']:
            print(f"Data Points: {len(data['data'].get('y', []))}")
            if data['data'].get('y'):
                print(f"First Price: ${data['data']['y'][0]}")
                print(f"Last Price: ${data['data']['y'][-1]}")
        else:
            print("No chart data available")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")