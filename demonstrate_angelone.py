import requests
import json

def demonstrate_angelone():
    """
    Demonstrate the Angel One style stock market assistant
    """
    print("🤖 ANGEL ONE STYLE STOCK MARKET ASSISTANT")
    print("=" * 50)
    
    # Example with AAPL stock
    symbol = "AAPL"
    print(f"Fetching real-time data for {symbol}...")
    
    try:
        # Get Angel One style data
        response = requests.get(f'http://127.0.0.1:5000/get_angelone_data?symbol={symbol}&period=1d')
        
        if response.status_code == 200:
            data = response.json()
            
            # Display Angel One style UI
            print("\n" + "=" * 50)
            print("📈 ANGEL ONE STYLE STOCK DASHBOARD")
            print("=" * 50)
            print(f"{data['symbol']} | {data['exchange']}")
            print("-" * 50)
            
            # Color coding for change
            change_indicator = "🟢" if data['change_abs'] >= 0 else "🔴"
            print(f"LTP: ${data['ltp']:.2f}")
            print(f"Change: {change_indicator} {data['change_abs']:.2f} ({data['change_pct']:.2f}%)")
            print("-" * 50)
            print("BUY [BUY]                    SELL [SELL]")
            print("-" * 50)
            print(f"Open:     ${data['open']:.2f}")
            print(f"High:     ${data['high']:.2f}")
            print(f"Low:      ${data['low']:.2f}")
            print(f"Prev Close: ${data['prev_close']:.2f}")
            print(f"Volume:   {data['volume']:,}")
            print(f"52W High: ${data['high_52w']:.2f}")
            print(f"52W Low:  ${data['low_52w']:.2f}")
            print("-" * 50)
            print(f"Chart Timeframe: [{data['selected_timeframe'].upper()}]")
            print("[1D] [1W] [1M] [3M] [6M] [1Y] [5Y]")
            print("=" * 50)
            
            # Display JSON data
            print("\n📄 JSON RESPONSE:")
            print(json.dumps(data, indent=2))
            
            print("\n✅ Demonstration complete!")
        else:
            print("❌ Error fetching data")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    demonstrate_angelone()