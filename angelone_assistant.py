import requests
import json

def get_angelone_data(symbol, period='1d'):
    """
    Fetch Angel One style stock data
    """
    try:
        response = requests.get(f'http://127.0.0.1:5000/get_angelone_data?symbol={symbol}&period={period}')
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'Live market data unavailable'}
    except Exception as e:
        return {'error': 'Live market data unavailable'}

def format_angelone_ui(data):
    """
    Format data in Angel One style UI text
    """
    if 'error' in data:
        return f"❌ {data['error']}"
    
    # Color coding for change
    change_color = "🟢" if data['change_abs'] >= 0 else "🔴"
    
    # Format the UI display
    ui_text = f"""
==================================================
📈 ANGEL ONE STYLE STOCK DASHBOARD
==================================================
{data['symbol']} | {data['exchange']}
--------------------------------------------------
LTP: ₹{data['ltp']:.2f}
Change: {change_color} {data['change_abs']:.2f} ({data['change_pct']:.2f}%)
--------------------------------------------------
BUY [BUY]                    SELL [SELL]
--------------------------------------------------
Open:     ₹{data['open']:.2f}
High:     ₹{data['high']:.2f}
Low:      ₹{data['low']:.2f}
Prev Close: ₹{data['prev_close']:.2f}
Volume:   {data['volume']:,}
52W High: ₹{data['high_52w']:.2f}
52W Low:  ₹{data['low_52w']:.2f}
--------------------------------------------------
Chart Timeframe: [{data['selected_timeframe'].upper()}]
[1D] [1W] [1M] [3M] [6M] [1Y] [5Y]
==================================================
"""
    return ui_text

def simulate_trading_flow(symbol):
    """
    Simulate the trading flow when user clicks BUY or SELL
    """
    print(f"\n🎯 TRADING FLOW SIMULATION FOR {symbol}")
    print("=" * 50)
    
    # Get order type
    print("1. Order Type:")
    print("   1. Delivery")
    print("   2. Intraday")
    order_type = input("   Select (1/2): ") or "1"
    order_type = "Delivery" if order_type == "1" else "Intraday"
    
    # Get order mode
    print("\n2. Order Mode:")
    print("   1. Market")
    print("   2. Limit")
    print("   3. SL")
    print("   4. SL-M")
    order_mode = input("   Select (1/2/3/4): ") or "1"
    modes = {"1": "Market", "2": "Limit", "3": "SL", "4": "SL-M"}
    order_mode = modes.get(order_mode, "Market")
    
    # Get quantity
    quantity = input("\n3. Quantity: ") or "1"
    
    # Get target and stop-loss for SL orders
    target = "N/A"
    stop_loss = "N/A"
    if order_mode in ["SL", "SL-M"]:
        target = input("\n4. Target: ") or "N/A"
        stop_loss = input("5. Stop Loss: ") or "N/A"
    
    # Show confirmation
    print("\n" + "=" * 50)
    print("✅ ORDER CONFIRMATION")
    print("=" * 50)
    print(f"Symbol: {symbol}")
    print(f"Order Type: {order_type}")
    print(f"Order Mode: {order_mode}")
    print(f"Quantity: {quantity}")
    if target != "N/A":
        print(f"Target: {target}")
    if stop_loss != "N/A":
        print(f"Stop Loss: {stop_loss}")
    print("=" * 50)
    print("⚠️  This is a simulation. No real trades executed.")
    print("=" * 50)

def main():
    print("🤖 ANGEL ONE STYLE STOCK MARKET ASSISTANT")
    print("Enter stock symbol to get real-time data")
    print("Type 'quit' to exit")
    
    while True:
        symbol = input("\nEnter stock symbol (e.g., AAPL, MSFT, GOOGL): ").strip().upper()
        
        if symbol.lower() == 'quit':
            print("👋 Goodbye!")
            break
            
        if not symbol:
            print("❌ Please enter a valid stock symbol")
            continue
            
        # Get data for default period (1D)
        print(f"\n🔍 Fetching data for {symbol}...")
        data = get_angelone_data(symbol, '1d')
        
        if 'error' in data:
            print(format_angelone_ui(data))
            continue
            
        # Display Angel One style UI
        print(format_angelone_ui(data))
        
        # Display JSON data
        print("\n📄 JSON DATA:")
        print(json.dumps(data, indent=2))
        
        # Ask if user wants to simulate trading
        trade = input("\nWould you like to simulate a trade? (y/n): ").strip().lower()
        if trade == 'y':
            simulate_trading_flow(symbol)

if __name__ == "__main__":
    main()