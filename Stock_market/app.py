from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import json
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Mock data structures (in a real app, you'd use a database)
MOCK_USERS = {
    'admin': {'username': 'admin', 'email': 'admin@example.com', 'password': 'admin123'},
    'user1': {'username': 'user1', 'email': 'user1@example.com', 'password': 'password123'},
    'praveen': {'username': 'praveen', 'email': 'praveen@example.com', 'password': '12'}
}

MOCK_PORTFOLIO = {
    'admin': [
        {'symbol': 'AAPL', 'quantity': 10, 'avg_price': 150.0},
        {'symbol': 'MSFT', 'quantity': 5, 'avg_price': 300.0}
    ],
    'user1': [
        {'symbol': 'GOOGL', 'quantity': 8, 'avg_price': 2500.0}
    ],
    'praveen': [
        {'symbol': 'TSLA', 'quantity': 3, 'avg_price': 700.0}
    ]
}

MOCK_TRADING_HISTORY = {
    'admin': [
        {
            'date': '2025-11-15 10:30:00',
            'symbol': 'AAPL',
            'action': 'buy',
            'quantity': 10,
            'price': 150.00
        },
        {
            'date': '2025-11-14 14:15:00',
            'symbol': 'MSFT',
            'action': 'buy',
            'quantity': 5,
            'price': 300.00
        },
        {
            'date': '2025-11-10 09:45:00',
            'symbol': 'GOOGL',
            'action': 'sell',
            'quantity': 3,
            'price': 2500.00
        }
    ],
    'user1': [
        {
            'date': '2025-11-05 11:20:00',
            'symbol': 'TSLA',
            'action': 'buy',
            'quantity': 2,
            'price': 700.00
        }
    ],
    'praveen': [
        {
            'date': '2025-11-01 13:10:00',
            'symbol': 'AMZN',
            'action': 'sell',
            'quantity': 1,
            'price': 3200.00
        }
    ]
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validate inputs
        if not username or not password:
            return render_template('login.html', error='Please enter both username and password')
        
        print(f"Login attempt: username={username}")
        
        # Try database first
        db_checked = False
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='1234',
                database='stock_trading'
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            db_checked = True
            
            if user:
                session['username'] = username
                print(f"Login successful via DB: {username}")
                return redirect(url_for('home'))
        except mysql.connector.Error as err:
            print(f"Database error during login: {err}")
            db_checked = False
        
        # Fallback to mock data
        if username in MOCK_USERS and MOCK_USERS[username]['password'] == password:
            session['username'] = username
            print(f"Login successful via MOCK: {username}")
            return redirect(url_for('home'))
        
        # Login failed
        if db_checked:
            print(f"Login failed: Invalid credentials for {username}")
        else:
            print(f"Login failed: User {username} not found in MOCK data")
        
        return render_template('login.html', error='Invalid username or password. Please try again.')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        print(f"Signup attempt: username={username}, email={email}")
        
        # Simple validation
        if not username or not email or not password:
            return render_template('signup.html', error='All fields are required')
        
        if len(username) < 2:
            return render_template('signup.html', error='Username must be at least 2 characters')
        
        if len(password) < 2:
            return render_template('signup.html', error='Password must be at least 2 characters')
        
        # Try database first
        db_created = False
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='1234',
                database='stock_trading'
            )
            cursor = conn.cursor(dictionary=True)
            
            # Check if user exists
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            existing_user = cursor.fetchone()
            
            if existing_user:
                cursor.close()
                conn.close()
                print(f"Signup failed: User already exists - {username}")
                return render_template('signup.html', error='Username or email already exists')
            
            # Create new user
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                          (username, email, password))
            conn.commit()
            cursor.close()
            conn.close()
            
            db_created = True
            print(f"Signup successful via DB: {username}")
            
        except mysql.connector.Error as err:
            print(f"Database error during signup: {err}")
            db_created = False
        
        # If DB failed, use mock data
        if not db_created:
            # Check if user exists in mock
            if username in MOCK_USERS:
                print(f"Signup failed: User exists in MOCK - {username}")
                return render_template('signup.html', error='Username already exists')
            
            # Check email
            for user_data in MOCK_USERS.values():
                if user_data.get('email') == email:
                    print(f"Signup failed: Email exists in MOCK - {email}")
                    return render_template('signup.html', error='Email already exists')
            
            # Create in mock
            MOCK_USERS[username] = {"username": username, "email": email, "password": password}
            print(f"Signup successful via MOCK: {username}")
        
        # Initialize portfolio
        MOCK_PORTFOLIO[username] = []
        MOCK_TRADING_HISTORY[username] = []
        
        # Success - redirect to login
        return render_template('login.html', 
            success=f'Account created! Login with username: {username} and password: {password}')
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            return render_template('forgot_password.html', error='Please enter your email address')
        
        # Check if email exists in database
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='1234',
                database='stock_trading'
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT username FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user:
                # In a real application, you would send an email here
                return render_template('login.html', 
                    success=f'Password reset instructions sent to {email}. Your username is: {user["username"]}')
            else:
                return render_template('forgot_password.html', error='Email not found in our records')
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            # Fallback to mock data
            pass
        
        # Check mock data
        for username, user_data in MOCK_USERS.items():
            if user_data.get('email') == email:
                return render_template('login.html', 
                    success=f'Your username is: {username}. Password: {user_data["password"]}')
        
        return render_template('forgot_password.html', error='Email not found in our records')
    
    return render_template('forgot_password.html')

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    # Get real market data for sentiment
    major_indices = ['SPY', 'QQQ', 'DIA']  # S&P 500, NASDAQ, Dow Jones ETFs
    market_data = []
    total_change = 0
    
    for symbol in major_indices:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period='5d')
            if len(hist) >= 2:
                current = float(hist['Close'].iloc[-1])
                previous = float(hist['Close'].iloc[-2])
                change_pct = ((current - previous) / previous) * 100
                total_change += change_pct
                market_data.append({
                    'symbol': symbol,
                    'change': change_pct
                })
        except:
            pass
    
    # Calculate market sentiment from real data
    if market_data:
        avg_change = total_change / len(market_data)
        market_sentiment_score = min(max((avg_change + 2) / 4, 0), 1)  # Normalize to 0-1
        if avg_change > 1:
            market_sentiment_label = "Bullish"
        elif avg_change < -1:
            market_sentiment_label = "Bearish"
        else:
            market_sentiment_label = "Neutral"
    else:
        market_sentiment_score = 0.5
        market_sentiment_label = "Neutral"
    
    # Real sector data
    sector_etfs = {
        "Technology": "XLK",
        "Healthcare": "XLV",
        "Financial": "XLF",
        "Energy": "XLE",
        "Consumer": "XLY"
    }
    
    sector_sentiment = {}
    for sector, etf in sector_etfs.items():
        try:
            stock = yf.Ticker(etf)
            hist = stock.history(period='5d')
            if len(hist) >= 2:
                current = float(hist['Close'].iloc[-1])
                previous = float(hist['Close'].iloc[-2])
                change_pct = ((current - previous) / previous) * 100
                score = min(max((change_pct + 2) / 4, 0), 1)
                
                if change_pct > 0.5:
                    label = "Bullish"
                elif change_pct < -0.5:
                    label = "Bearish"
                else:
                    label = "Neutral"
                
                sector_sentiment[sector] = {"score": round(score, 2), "label": label}
            else:
                sector_sentiment[sector] = {"score": 0.5, "label": "Neutral"}
        except:
            sector_sentiment[sector] = {"score": 0.5, "label": "Neutral"}
    
    # Generate dynamic news based on real stock movements
    articles = []
    current_date = datetime.now().strftime('%B %d, %Y')
    
    # Get top movers
    top_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META']
    movers = []
    
    for symbol in top_stocks:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period='5d')
            if len(hist) >= 2:
                current = float(hist['Close'].iloc[-1])
                previous = float(hist['Close'].iloc[-2])
                change_pct = ((current - previous) / previous) * 100
                info = stock.info
                name = info.get('shortName', symbol)
                movers.append({
                    'symbol': symbol,
                    'name': name,
                    'change': change_pct,
                    'price': current * 83.0
                })
        except:
            pass
    
    # Sort by absolute change
    movers.sort(key=lambda x: abs(x['change']), reverse=True)
    
    # Create news from top 3 movers
    if len(movers) >= 1:
        top = movers[0]
        direction = "surges" if top['change'] > 0 else "drops"
        articles.append({
            "title": f"{top['name']} {direction} {abs(top['change']):.1f}% - {current_date}",
            "summary": f"{top['name']} ({top['symbol']}) shows significant movement with {top['change']:.2f}% change. Current price: ₹{top['price']:.2f}. Market analysts monitoring closely."
        })
    
    if len(movers) >= 2:
        second = movers[1]
        direction = "rallies" if second['change'] > 0 else "declines"
        articles.append({
            "title": f"{second['name']} {direction} {abs(second['change']):.1f}% in Latest Trading",
            "summary": f"{second['name']} experiences {abs(second['change']):.2f}% {'gain' if second['change'] > 0 else 'loss'} at ₹{second['price']:.2f}. Trading volume indicates strong investor interest."
        })
    
    # Add market overview
    if market_sentiment_label == "Bullish":
        articles.append({
            "title": f"Markets Close Higher - {current_date}",
            "summary": f"Major indices show positive momentum with markets trending {market_sentiment_label.lower()}. Technology and growth stocks lead the rally as investor sentiment remains strong."
        })
    elif market_sentiment_label == "Bearish":
        articles.append({
            "title": f"Market Pullback Continues - {current_date}",
            "summary": f"Indices face pressure with {market_sentiment_label.lower()} sentiment prevailing. Investors rotating into defensive sectors amid market volatility."
        })
    else:
        articles.append({
            "title": f"Markets Trade Mixed - {current_date}",
            "summary": f"Indices show mixed performance with {market_sentiment_label.lower()} sentiment. Investors await key economic data and corporate earnings reports."
        })
    
    # Add fallback if no articles generated
    if not articles:
        articles = [
            {
                "title": f"Market Update - {current_date}",
                "summary": "Markets are currently active. Check individual stocks for latest price movements and trading opportunities."
            }
        ]
    
    return render_template('home.html', 
                         username=username,
                         market_sentiment_score=market_sentiment_score,
                         market_sentiment_label=market_sentiment_label,
                         sector_sentiment=sector_sentiment,
                         articles=articles)

@app.route('/portfolio')
def portfolio():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    # Get user's portfolio
    user_portfolio = MOCK_PORTFOLIO.get(username, [])
    
    # Calculate portfolio metrics
    total_invested = 0
    total_current_value = 0
    portfolio_details = []
    best_performance = float('-inf')
    best_performer = None
    
    for item in user_portfolio:
        symbol = item['symbol']
        quantity = item['quantity']
        avg_price = item['avg_price']
        
        # Get current price using yfinance
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="1d")
            if not hist.empty:
                current_price = float(hist['Close'].iloc[-1]) * 83.0  # Convert to INR
            else:
                current_price = avg_price * 83.0  # Fallback to avg price if no data
        except:
            current_price = avg_price * 83.0  # Fallback to avg price if error
        
        # Calculate metrics with INR conversion
        invested_amount = quantity * avg_price * 83.0  # Convert to INR
        current_value = quantity * current_price
        profit_loss = current_value - invested_amount
        return_rate = ((current_value - invested_amount) / invested_amount * 100) if invested_amount > 0 else 0
        
        # Update best performer
        if return_rate > best_performance:
            best_performance = return_rate
            best_performer = symbol
        
        # Add to totals
        total_invested += invested_amount
        total_current_value += current_value
        
        # Add to portfolio details
        portfolio_details.append({
            'symbol': symbol,
            'quantity': quantity,
            'avg_price': avg_price * 83.0,  # Convert to INR
            'current_price': current_price,
            'return_rate': return_rate,
            'current_value': current_value,
            'profit_loss': profit_loss
        })
    
    # Calculate overall metrics
    total_profit_loss = total_current_value - total_invested
    overall_return_rate = ((total_current_value - total_invested) / total_invested * 100) if total_invested > 0 else 0
    
    # If no holdings, set default values
    if best_performer is None:
        best_performer = "N/A"
        best_performance = 0
    
    # Create portfolio metrics object
    portfolio_metrics = {
        'total_current_value': total_current_value,
        'total_profit_loss': total_profit_loss,
        'overall_return_rate': overall_return_rate,
        'total_invested': total_invested,
        'best_performer': best_performer,
        'best_performance': best_performance,
        'last_updated': datetime.now(),
        'portfolio_details': portfolio_details
    }
    
    return render_template('portfolio.html', 
                         username=username,
                         portfolio_metrics=portfolio_metrics)

@app.route('/add_to_portfolio', methods=['POST'])
def add_to_portfolio():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'User not logged in'})
    
    username = session['username']
    
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        quantity = data.get('quantity')
        avg_price = data.get('avg_price')
        
        # Validate inputs
        if not symbol or not quantity or not avg_price:
            return jsonify({'success': False, 'message': 'Missing required fields'})
        
        # Ensure user has a portfolio
        if username not in MOCK_PORTFOLIO:
            MOCK_PORTFOLIO[username] = []
        
        # Add to portfolio
        MOCK_PORTFOLIO[username].append({
            'symbol': symbol.upper(),
            'quantity': int(quantity),
            'avg_price': float(avg_price)
        })
        
        return jsonify({'success': True, 'message': f'Successfully added {symbol} to portfolio'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error adding to portfolio: {str(e)}'})

@app.route('/trade')
def trade():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('trade.html', username=session['username'])

@app.route('/execute_trade', methods=['POST'])
def execute_trade():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'User not logged in'}), 401
    
    username = session['username']
    
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').strip().upper()
        action = data.get('action', '').lower()
        quantity = int(data.get('quantity', 0))
        price = float(data.get('price', 0))
        
        print(f"Trade execution: user={username}, symbol={symbol}, action={action}, qty={quantity}, price={price}")
        
        # Validate inputs
        if not symbol or action not in ['buy', 'sell'] or quantity <= 0 or price <= 0:
            return jsonify({'success': False, 'message': 'Invalid trade parameters'}), 400
        
        # Create trade record
        trade_record = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'symbol': symbol,
            'action': action,
            'quantity': quantity,
            'price': round(price, 2)
        }
        
        # Initialize user's trading history if not exists
        if username not in MOCK_TRADING_HISTORY:
            MOCK_TRADING_HISTORY[username] = []
        
        # Add trade to history
        MOCK_TRADING_HISTORY[username].insert(0, trade_record)  # Add to beginning
        
        # Update portfolio
        if username not in MOCK_PORTFOLIO:
            MOCK_PORTFOLIO[username] = []
        
        portfolio = MOCK_PORTFOLIO[username]
        
        if action == 'buy':
            # Find existing position
            existing = None
            for item in portfolio:
                if item['symbol'] == symbol:
                    existing = item
                    break
            
            if existing:
                # Update existing position
                total_cost = (existing['quantity'] * existing['avg_price']) + (quantity * price)
                existing['quantity'] += quantity
                existing['avg_price'] = total_cost / existing['quantity']
            else:
                # Create new position
                portfolio.append({
                    'symbol': symbol,
                    'quantity': quantity,
                    'avg_price': price
                })
        
        elif action == 'sell':
            # Find existing position
            existing = None
            for item in portfolio:
                if item['symbol'] == symbol:
                    existing = item
                    break
            
            if existing:
                if existing['quantity'] >= quantity:
                    existing['quantity'] -= quantity
                    # Remove if quantity becomes zero
                    if existing['quantity'] == 0:
                        portfolio.remove(existing)
                else:
                    return jsonify({
                        'success': False, 
                        'message': f'Insufficient shares. You have {existing["quantity"]} shares of {symbol}'
                    }), 400
            else:
                return jsonify({
                    'success': False, 
                    'message': f'You don\'t own any shares of {symbol}'
                }), 400
        
        # Try to save to database
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='1234',
                database='stock_trading'
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO trading_history (username, symbol, action, quantity, price, trade_date) VALUES (%s, %s, %s, %s, %s, %s)",
                (username, symbol, action, quantity, price, trade_record['date'])
            )
            conn.commit()
            cursor.close()
            conn.close()
            print(f"Trade saved to database: {symbol} {action}")
        except mysql.connector.Error as err:
            print(f"Database error saving trade: {err}")
            # Continue anyway, data is in MOCK
        
        print(f"Trade executed successfully: {symbol} {action} {quantity} @ {price}")
        
        return jsonify({
            'success': True,
            'message': f'Trade completed successfully! {action.upper()} {quantity} shares of {symbol} at ₹{price:.2f}',
            'trade': trade_record
        })
        
    except Exception as e:
        print(f"Error executing trade: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Trade failed: {str(e)}'
        }), 500

@app.route('/stock_graph')
def stock_graph():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    symbol = request.args.get('symbol', 'AAPL')
    period = request.args.get('period', '1d')
    
    return render_template('stock_graph.html', 
                         username=username,
                         symbol=symbol,
                         period=period)

@app.route('/predict_next_week')
def predict_next_week():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    # Sample stock symbols for predictions
    stock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'AMD', 'INTC']
    
    go_high_predictions = []
    go_low_predictions = []
    neutral_predictions = []
    
    # Generate predictions for each stock
    for symbol in stock_symbols:
        try:
            # Fetch stock data using yfinance
            stock = yf.Ticker(symbol)
            hist = stock.history(period="3mo")
            
            if hist.empty:
                continue
                
            # Get current price
            current_price = float(hist['Close'].iloc[-1])
            
            # Calculate technical indicators
            # Moving averages
            hist['MA20'] = hist['Close'].rolling(window=20).mean()
            hist['MA50'] = hist['Close'].rolling(window=50).mean()
            
            ma20 = hist['MA20'].iloc[-1]
            ma50 = hist['MA50'].iloc[-1]
            
            # RSI calculation
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            rsi_value = 50.0  # Default
            try:
                rsi_value = float(rsi.iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
            except:
                try:
                    rsi_value = float(pd.Series(rsi).iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
                except:
                    pass
            
            # Get company name
            try:
                info = stock.info
                company_name = info.get('longName', symbol)
            except:
                company_name = symbol
            
            # Simple prediction logic
            buy_signals = 0
            sell_signals = 0
            
            # Moving average signals
            if current_price > ma20:
                buy_signals += 1
            else:
                sell_signals += 1
                
            if ma20 > ma50:
                buy_signals += 1
            else:
                sell_signals += 1
                
            # RSI signals
            if rsi_value < 30:
                buy_signals += 1
            elif rsi_value > 70:
                sell_signals += 1
            else:
                # Neutral RSI
                pass
            
            # Create prediction object
            prediction = {
                'symbol': symbol,
                'name': company_name,
                'current_price': current_price,
                'rsi': round(rsi_value, 2),
                'buy_signals': buy_signals,
                'sell_signals': sell_signals,
                'recommendation': 'Strong Buy' if buy_signals >= 2 else ('Strong Sell' if sell_signals >= 2 else 'Hold')
            }
            
            # Categorize predictions
            if buy_signals >= 2:
                go_high_predictions.append(prediction)
            elif sell_signals >= 2:
                go_low_predictions.append(prediction)
            else:
                neutral_predictions.append(prediction)
                
        except Exception as e:
            print(f"Error generating prediction for {symbol}: {e}")
            continue
    
    return render_template('predict_next_week.html', 
                         username=username,
                         go_high_predictions=go_high_predictions,
                         go_low_predictions=go_low_predictions,
                         neutral_predictions=neutral_predictions)

@app.route('/prediction_chart/<symbol>')
def prediction_chart(symbol):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    try:
        # Fetch stock data using yfinance
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1mo")  # Last 30 days for historical data
        
        if hist.empty:
            return render_template('prediction_chart.html', 
                                 username=username,
                                 error="No data available for this stock symbol")
        
        # Get current price and company name
        current_price = float(hist['Close'].iloc[-1]) * 83.0  # Convert to INR
        try:
            info = stock.info
            company_name = info.get('longName', symbol)
        except:
            company_name = symbol
        
        # Prepare historical data
        historical_dates = [idx.strftime('%Y-%m-%d') for idx in hist.index]
        historical_prices = [float(val) * 83.0 for val in hist['Close']]  # Convert to INR
        historical_ma20 = [float(val) * 83.0 if not pd.isna(val) else None for val in hist['MA20']] if 'MA20' in hist.columns else []
        historical_ma50 = [float(val) * 83.0 if not pd.isna(val) else None for val in hist['MA50']] if 'MA50' in hist.columns else []
        
        # Calculate RSI for historical data
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi_series = 100 - (100 / (1 + rs))
        # Convert to list safely
        historical_rsi = []
        try:
            # Handle case where rsi_series might be a scalar by converting to Series
            # pyright: ignore[reportAttributeAccessIssue, reportArgumentType]
            if isinstance(rsi_series, (int, float)) or (hasattr(rsi_series, 'ndim') and rsi_series.ndim == 0):
                rsi_series = pd.Series([float(rsi_series)] * len(historical_dates))
            elif not isinstance(rsi_series, pd.Series):
                rsi_series = pd.Series(rsi_series)
            
            for i in range(len(rsi_series)):
                val = rsi_series.iloc[i]  # pyright: ignore[reportAttributeAccessIssue]
                if not pd.isna(val):
                    historical_rsi.append(float(val))
                else:
                    historical_rsi.append(None)
        except:
            # Fallback if the above approach doesn't work
            historical_rsi = [50.0] * len(historical_dates)
        
        # Simple prediction for next 7 days (mock data for now)
        # In a real application, this would use a machine learning model
        prediction_dates = []
        prediction_prices = []
        last_date = hist.index[-1]
        
        # Generate 7 days of prediction data
        for i in range(1, 8):
            next_date = last_date + timedelta(days=i)
            prediction_dates.append(next_date.strftime('%Y-%m-%d'))
            # Simple linear prediction based on recent trend
            price_change = (historical_prices[-1] - historical_prices[-2]) if len(historical_prices) > 1 else 0
            predicted_price = historical_prices[-1] + (price_change * i * 0.8)  # Dampen the prediction
            prediction_prices.append(float(predicted_price))
        
        # Prepare moving averages for predictions (simplified)
        prediction_ma20 = [float(val) for val in prediction_prices]  # Simplified
        prediction_rsi = [historical_rsi[-1]] * 7 if historical_rsi and historical_rsi[-1] is not None else [50.0] * 7  # Simplified - keep last RSI value
        
        return render_template('prediction_chart.html',
                             username=username,
                             symbol=symbol,
                             company_name=company_name,
                             current_price=current_price,
                             currency_symbol='₹',
                             historical_dates=json.dumps(historical_dates),
                             historical_prices=json.dumps(historical_prices),
                             historical_ma20=json.dumps(historical_ma20),
                             historical_ma50=json.dumps(historical_ma50),
                             historical_rsi=json.dumps(historical_rsi),
                             historical_bb_upper=json.dumps([]),  # Simplified
                             historical_bb_lower=json.dumps([]),  # Simplified
                             prediction_dates=json.dumps(prediction_dates),
                             prediction_prices=json.dumps(prediction_prices),
                             prediction_ma20=json.dumps(prediction_ma20),
                             prediction_rsi=json.dumps(prediction_rsi))
                             
    except Exception as e:
        print(f"Error generating prediction chart for {symbol}: {e}")
        return render_template('prediction_chart.html', 
                             username=username,
                             error="Error loading chart data")

@app.route('/trading_history')
def trading_history():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    # Initialize if not exists
    if username not in MOCK_TRADING_HISTORY:
        MOCK_TRADING_HISTORY[username] = []
    
    # Get user's trading history
    user_trading_history = MOCK_TRADING_HISTORY[username]
    
    print(f"Trading history for {username}: {len(user_trading_history)} trades")
    
    return render_template('trading_history.html', 
                         username=username,
                         trading_history=user_trading_history)

@app.route('/sentiment_analysis')
def sentiment_analysis():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    # Mock market sentiment data
    market_sentiment_score = 0.65  # 65% bullish sentiment
    market_sentiment_label = "Bullish"
    
    # Mock sector sentiment data
    sector_sentiment = {
        "Technology": {"score": 0.75, "label": "Bullish"},
        "Healthcare": {"score": 0.45, "label": "Bearish"},
        "Financial": {"score": 0.60, "label": "Bullish"},
        "Energy": {"score": 0.35, "label": "Bearish"},
        "Consumer": {"score": 0.55, "label": "Neutral"}
    }
    
    # Mock trending stocks based on sentiment
    trending_stocks = [
        ("AAPL", {"score": 0.85, "label": "Bullish"}),
        ("TSLA", {"score": 0.78, "label": "Bullish"}),
        ("AMZN", {"score": 0.72, "label": "Bullish"}),
        ("GOOGL", {"score": 0.68, "label": "Bullish"}),
        ("MSFT", {"score": 0.65, "label": "Bullish"})
    ]
    
    # Mock stock sentiments
    stock_sentiments = {
        "AAPL": {"score": 0.85, "label": "Bullish", "articles": [
            {"title": "Apple Q3 Earnings Beat Expectations", "summary": "Strong iPhone sales drive record quarterly revenue"},
            {"title": "Apple Announces New AI Features", "summary": "Innovative machine learning capabilities unveiled at developer conference"}
        ]},
        "MSFT": {"score": 0.75, "label": "Bullish", "articles": [
            {"title": "Microsoft Cloud Revenue Surges", "summary": "Azure platform shows 30% year-over-year growth"},
            {"title": "Microsoft Acquires AI Startup", "summary": "Strategic acquisition strengthens AI capabilities"}
        ]},
        "GOOGL": {"score": 0.68, "label": "Bullish", "articles": [
            {"title": "Google Search Ad Revenue Increases", "summary": "Strong performance in key advertising segments"},
            {"title": "Google Expands Cloud Services", "summary": "New data centers announced for global expansion"}
        ]},
        "AMZN": {"score": 0.72, "label": "Bullish", "articles": [
            {"title": "Amazon Prime Membership Growth", "summary": "Record number of subscribers drives revenue"},
            {"title": "Amazon Expands Logistics Network", "summary": "New fulfillment centers to improve delivery times"}
        ]},
        "TSLA": {"score": 0.78, "label": "Bullish", "articles": [
            {"title": "Tesla Announces New Factory", "summary": "Electric vehicle production capacity to expand significantly"},
            {"title": "Tesla Battery Technology Breakthrough", "summary": "New innovation promises longer range vehicles"}
        ]}
    }
    
    # Mock news articles
    articles = [
        {
            "title": "Tech Stocks Rally on Strong Earnings Reports",
            "summary": "Major technology companies exceeded Q3 earnings expectations, driving a broad market rally. Analysts predict continued growth in the sector."
        },
        {
            "title": "Federal Reserve Holds Interest Rates Steady",
            "summary": "The Federal Reserve maintained current interest rates following their latest policy meeting, citing stable inflation data. Markets responded positively to the decision."
        },
        {
            "title": "Oil Prices Drop Amid Supply Concerns",
            "summary": "Global oil prices fell 3% as supply chain disruptions ease and demand forecasts are revised downward. Energy sector stocks declined accordingly."
        },
        {
            "title": "Consumer Spending Remains Strong Despite Inflation",
            "summary": "Retail sales data shows continued consumer confidence despite ongoing inflationary pressures. Analysts revise GDP growth forecasts upward."
        },
        {
            "title": "Cryptocurrency Market Shows Signs of Recovery",
            "summary": "Bitcoin and other major cryptocurrencies show positive momentum following regulatory clarity from financial authorities."
        }
    ]
    
    return render_template('sentiment_analysis.html', 
                         username=username,
                         market_sentiment_score=market_sentiment_score,
                         market_sentiment_label=market_sentiment_label,
                         sector_sentiment=sector_sentiment,
                         trending_stocks=trending_stocks,
                         stock_sentiments=stock_sentiments,
                         articles=articles)

@app.route('/get_trading_signal')
def get_trading_signal():
    symbol = request.args.get('symbol', 'AAPL')
    
    # Simple trading signal logic (in a real app, this would be more sophisticated)
    try:
        # Fetch stock data
        stock = yf.Ticker(symbol)
        hist = stock.history(period="3mo")
        
        if hist.empty:
            return jsonify({
                'signal': 'HOLD',
                'reason': 'No data available'
            })
        
        # Calculate simple moving averages
        hist['MA20'] = hist['Close'].rolling(window=20).mean()
        hist['MA50'] = hist['Close'].rolling(window=50).mean()
        
        current_price = hist['Close'].iloc[-1]
        ma20 = hist['MA20'].iloc[-1]
        ma50 = hist['MA50'].iloc[-1]
        
        # Simple signal logic
        if current_price > ma20 and ma20 > ma50:
            signal = 'BUY'
            reason = f'GO HIGH: Price: ₹{current_price * 83:.2f} | Bullish trend'
        elif current_price < ma20 and ma20 < ma50:
            signal = 'SELL'
            reason = f'GO LOW: Price: ₹{current_price * 83:.2f} | Bearish trend'
        else:
            signal = 'HOLD'
            reason = f'NEUTRAL: Price: ₹{current_price * 83:.2f} | Wait for clearer signal'
        
        return jsonify({
            'signal': signal,
            'reason': reason
        })
    except Exception as e:
        print(f"Error generating trading signal for {symbol}: {e}")
        return jsonify({
            'signal': 'HOLD',
            'reason': 'Error generating signal'
        })

@app.route('/get_chart_data')
def get_chart_data():
    symbol = request.args.get('symbol', 'AAPL')
    period = request.args.get('period', '1y')
    
    try:
        # Map period to yfinance period
        period_map = {
            '1d': '1d',
            '1wk': '5d',
            '1w': '5d',
            '1mo': '1mo',
            '1m': '1mo',
            '3mo': '3mo',
            '3m': '3mo',
            '6mo': '6mo',
            '6m': '6mo',
            '1y': '1y',
            '5y': '5y',
            'max': 'max',
            'all': 'max'
        }
        
        # Map period to interval
        interval_map = {
            '1d': '5m',      # 5-minute intervals for 1 day
            '1wk': '30m',    # 30-minute intervals for 1 week
            '1w': '30m',
            '1mo': '1d',     # 1-day intervals for 1 month
            '1m': '1d',
            '3mo': '1d',
            '3m': '1d',
            '6mo': '1d',
            '6m': '1d',
            '1y': '1d',
            '5y': '1wk',
            'max': '1wk',
            'all': '1wk'
        }
        
        yf_period = period_map.get(period, '1y')
        yf_interval = interval_map.get(period, '1d')
        
        print(f"Fetching chart data for {symbol}, period={period}, yf_period={yf_period}, yf_interval={yf_interval}")
        
        # Fetch stock data
        stock = yf.Ticker(symbol)
        hist = stock.history(period=yf_period, interval=yf_interval)
        
        # If no data, try with default 1-month period
        if hist.empty:
            print(f"No data with period={yf_period}, trying 1mo")
            hist = stock.history(period='1mo', interval='1d')
        
        if hist.empty:
            print(f"Still no data for {symbol}")
            return jsonify({
                'error': 'No data available',
                'symbol': symbol
            }), 404
        
        # Convert to Indian Rupees and prepare data
        dates = []
        for idx in hist.index:
            try:
                dates.append(idx.strftime('%Y-%m-%d %H:%M:%S'))
            except:
                dates.append(str(idx))
        
        prices = [float(val) * 83.0 for val in hist['Close']]  # Convert to INR
        highs = [float(val) * 83.0 for val in hist['High']]  # Convert to INR
        lows = [float(val) * 83.0 for val in hist['Low']]  # Convert to INR
        
        # Calculate technical indicators for chart overlay
        # Moving Averages (only for periods longer than 1 day)
        ma20 = [None] * len(prices)
        ma50 = [None] * len(prices)
        rsi = [50.0] * len(prices)
        
        if period != '1d' and len(hist) >= 20:
            hist['MA20'] = hist['Close'].rolling(window=min(20, len(hist))).mean()
            hist['MA50'] = hist['Close'].rolling(window=min(50, len(hist))).mean()
            
            # Convert moving averages to INR
            ma20 = [float(val) * 83.0 if not pd.isna(val) else None for val in hist['MA20']]
            ma50 = [float(val) * 83.0 if not pd.isna(val) else None for val in hist['MA50']]
            
            # RSI calculation
            if len(hist) >= 14:
                delta = hist['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi_series = 100 - (100 / (1 + rs))
                
                # Convert RSI to list
                rsi = []
                try:
                    # Handle case where rsi_series might be a scalar by converting to Series
                    # pyright: ignore[reportAttributeAccessIssue, reportArgumentType]
                    if isinstance(rsi_series, (int, float)) or (hasattr(rsi_series, 'ndim') and rsi_series.ndim == 0):
                        rsi_series = pd.Series([float(rsi_series)] * len(dates))
                    elif not isinstance(rsi_series, pd.Series):
                        rsi_series = pd.Series(rsi_series)
                    
                    for i in range(len(rsi_series)):
                        val = rsi_series.iloc[i]  # pyright: ignore[reportAttributeAccessIssue]
                        if not pd.isna(val):
                            rsi.append(float(val))
                        else:
                            rsi.append(None)
                except:
                    # Fallback if the above approach doesn't work
                    rsi = [50.0] * len(dates)
        
        # Enhanced AI features
        # Calculate volatility
        if len(prices) > 1:
            returns = []
            for i in range(1, len(prices)):
                returns.append((prices[i] - prices[i-1]) / prices[i-1])
            volatility = np.std(returns) * np.sqrt(252) if len(returns) > 1 else 0
        else:
            volatility = 0
        
        # Calculate trend direction
        if len(prices) > 1:
            price_change = prices[-1] - prices[0]
            trend_direction = "Bullish" if price_change > 0 else "Bearish" if price_change < 0 else "Neutral"
        else:
            trend_direction = "Neutral"
        
        # Calculate support and resistance levels (only for longer periods)
        support_level = 0
        resistance_level = 0
        if period != '1d' and len(prices) > 0:
            support_level = min(prices) * 0.99
            resistance_level = max(prices) * 1.01
        
        # Calculate next day prediction
        if len(prices) > 1:
            # Simple momentum-based prediction
            recent_changes = []
            for i in range(max(0, len(prices) - 10), len(prices)):
                if i > 0:
                    recent_changes.append(prices[i] - prices[i-1])
            
            if len(recent_changes) > 0:
                avg_change = sum(recent_changes) / len(recent_changes)
                # Add some randomness based on volatility
                volatility_factor = volatility * prices[-1] * 0.1
                random_factor = np.random.normal(0, volatility_factor)
                next_day_prediction = prices[-1] + avg_change + random_factor
            else:
                next_day_prediction = prices[-1]
        else:
            next_day_prediction = prices[-1] if prices else 0
        
        print(f"Successfully fetched {len(dates)} data points for {symbol}")
        
        return jsonify({
            'symbol': symbol,
            'data': {
                'x': dates,
                'y': prices,
                'ma20': ma20,
                'ma50': ma50,
                'rsi': rsi
            },
            'high': highs,
            'low': lows,
            'ai_features': {
                'volatility': round(volatility, 4),
                'trend_direction': trend_direction,
                'support_level': round(support_level, 2),
                'resistance_level': round(resistance_level, 2),
                'next_day_prediction': round(next_day_prediction, 2),
                'data_points': len(dates)
            }
        })
    except Exception as e:
        print(f"Error fetching chart data for {symbol}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Error loading chart data',
            'message': str(e),
            'symbol': symbol
        }), 500

@app.route('/get_multiple_stock_data')
def get_multiple_stock_data():
    symbols = request.args.get('symbols', 'AAPL,MSFT,GOOGL')
    symbol_list = symbols.split(',')
    
    stock_data = []
    
    for symbol in symbol_list:
        try:
            # Fetch stock data using yfinance
            stock = yf.Ticker(symbol.strip())
            
            # Try to get the most recent data (1 day with 1-minute intervals for maximum recency)
            hist = stock.history(period="1d", interval="1m")
            
            # If no 1-minute data, try hourly data
            if hist.empty:
                hist = stock.history(period="5d", interval="1h")
                
            # If still empty, fallback to daily data
            if hist.empty:
                hist = stock.history(period="1mo")
                
            if hist.empty:
                stock_data.append({
                    'symbol': symbol.strip(),
                    'price': 0.0,
                    'change': 0.0,
                    'changePercent': 0.0,
                    'name': symbol.strip()
                })
                continue
            
            # Get the latest price (current market price)
            current_price = float(hist['Close'].iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
            
            # Calculate change from previous close
            if len(hist) > 1:
                previous_price = float(hist['Close'].iloc[-2])  # pyright: ignore[reportAttributeAccessIssue]
                change = current_price - previous_price
                change_percent = (change / previous_price) * 100
            else:
                change = 0.0
                change_percent = 0.0
                
            # Get company name
            try:
                info = stock.info
                company_name = info.get('longName', symbol.strip())
            except:
                company_name = symbol.strip()
                
            # Ensure all values are proper floats
            current_price = float(current_price)
            change = float(change)
            change_percent = float(change_percent)
                
            stock_data.append({
                'symbol': symbol.strip(),
                'price': round(current_price * 83.0, 2),
                'change': round(change * 83.0, 2),
                'changePercent': round(change_percent, 2),
                'name': company_name
            })
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            # Return default data in case of error
            stock_data.append({
                'symbol': symbol.strip(),
                'price': 8300.00,
                'change': 0.00,
                'changePercent': 0.00,
                'name': symbol.strip()
            })
    
    return jsonify(stock_data)

@app.route('/get_1d_prediction')
def get_1d_prediction():
    symbol = request.args.get('symbol', 'AAPL')
    
    try:
        # Fetch stock data
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1mo")
        
        if hist.empty:
            return jsonify({
                'prediction': 'HOLD',
                'reason': 'No data available',
                'predicted_price': 0
            })
        
        # Simple prediction logic (in a real app, this would be more sophisticated)
        current_price = hist['Close'].iloc[-1]
        previous_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        
        # Calculate simple moving averages
        hist['MA20'] = hist['Close'].rolling(window=20).mean()
        hist['MA50'] = hist['Close'].rolling(window=50).mean()
        
        ma20 = hist['MA20'].iloc[-1]
        ma50 = hist['MA50'].iloc[-1]
        
        # RSI calculation
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        # Extract RSI value safely with default fallback
        rsi_value = 50.0  # Default neutral RSI value

        # Simple approach to avoid linter errors
        try:
            rsi_value = float(rsi.iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        except:
            try:
                rsi_value = float(pd.Series(rsi).iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
            except:
                pass  # Keep default value
        
        # Simple price prediction based on trend
        price_change = current_price - previous_price
        momentum = price_change / previous_price
        
        # Predict next day price (simple linear extrapolation with dampening)
        predicted_price_usd = current_price + (price_change * 0.5)  # 50% dampening factor
        predicted_price_inr = predicted_price_usd * 83.0  # Convert to INR
        
        # Simple prediction logic
        if current_price > ma20 and ma20 > ma50 and rsi_value < 70:
            prediction = 'BUY'
            reason = f'GO HIGH: Current: ₹{current_price * 83:.2f} | Predicted: ₹{predicted_price_inr:.2f} | RSI: {rsi_value:.1f}'
        elif current_price < ma20 and ma20 < ma50 and rsi_value > 30:
            prediction = 'SELL'
            reason = f'GO LOW: Current: ₹{current_price * 83:.2f} | Predicted: ₹{predicted_price_inr:.2f} | RSI: {rsi_value:.1f}'
        else:
            prediction = 'HOLD'
            reason = f'NEUTRAL: Current: ₹{current_price * 83:.2f} | Predicted: ₹{predicted_price_inr:.2f} | RSI: {rsi_value:.1f}'
        
        return jsonify({
            'prediction': prediction,
            'reason': reason,
            'predicted_price': round(predicted_price_inr, 2),
            'current_price': round(current_price * 83.0, 2),
            'rsi': round(rsi_value, 2)
        })
    except Exception as e:
        print(f"Error generating prediction for {symbol}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'prediction': 'HOLD',
            'reason': 'Error generating prediction',
            'predicted_price': 0
        })

@app.route('/get_stock_data')
def get_stock_data():
    symbol = request.args.get('symbol', 'AAPL')
    
    try:
        # Fetch stock data using yfinance
        stock = yf.Ticker(symbol)
        
        # Try to get the most recent data (1 day with 1-minute intervals for maximum recency)
        hist = stock.history(period="1d", interval="1m")
        
        # If no 1-minute data, try hourly data
        if hist.empty:
            hist = stock.history(period="5d", interval="1h")
            
        # If still empty, fallback to daily data
        if hist.empty:
            hist = stock.history(period="1mo")
            
        if hist.empty:
            return jsonify({
                'symbol': symbol,
                'price': 0.0,
                'change': 0.0,
                'changePercent': 0.0,
                'name': symbol
            })
        
        # Get the latest price (current market price)
        current_price = float(hist['Close'].iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        
        # Calculate change from previous close
        if len(hist) > 1:
            previous_price = float(hist['Close'].iloc[-2])  # pyright: ignore[reportAttributeAccessIssue]
            change = current_price - previous_price
            change_percent = (change / previous_price) * 100
        else:
            change = 0.0
            change_percent = 0.0
            
        # Get company name
        try:
            info = stock.info
            company_name = info.get('longName', symbol)
        except:
            company_name = symbol
            
        # Ensure all values are proper floats
        current_price = float(current_price)
        change = float(change)
        change_percent = float(change_percent)
            
        return jsonify({
            'symbol': symbol,
            'price': round(current_price * 83.0, 2),
            'change': round(change * 83.0, 2),
            'changePercent': round(change_percent, 2),
            'name': company_name
        })
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        # Return default data in case of error
        return jsonify({
            'symbol': symbol,
            'price': 8300.00,
            'change': 0.00,
            'changePercent': 0.00,
            'name': symbol
        })

@app.route('/get_technical_indicators')
def get_technical_indicators():
    symbol = request.args.get('symbol', 'AAPL')
    period = request.args.get('period', '1y')  # Get period parameter
    
    try:
        # Map period to yfinance period
        period_map = {
            '1d': '1d',
            '1w': '5d',
            '1m': '1mo',
            '1mo': '1mo',
            '3m': '3mo',
            '1y': '1y',
            'all': 'max'
        }
        
        yf_period = period_map.get(period, '1y')
        
        # Fetch stock data using yfinance
        stock = yf.Ticker(symbol)
        hist = stock.history(period=yf_period)
        
        if hist.empty:
            return jsonify({
                'error': 'No data available'
            }), 404
        
        # Calculate technical indicators
        # Moving Averages
        hist['MA20'] = hist['Close'].rolling(window=20).mean()
        hist['MA50'] = hist['Close'].rolling(window=50).mean()
        hist['MA200'] = hist['Close'].rolling(window=200).mean()
        hist['EMA12'] = hist['Close'].ewm(span=12).mean()  # pyright: ignore[reportAttributeAccessIssue]
        hist['EMA26'] = hist['Close'].ewm(span=26).mean()  # pyright: ignore[reportAttributeAccessIssue]
        
        # Current values
        current_price = float(hist['Close'].iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        ma20 = float(hist['MA20'].iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        ma50 = float(hist['MA50'].iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        ma200 = float(hist['MA200'].iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        ema12 = float(hist['EMA12'].iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        ema26 = float(hist['EMA26'].iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        
        # RSI
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        # Extract RSI value safely with default fallback
        rsi_value = 50.0  # Default neutral RSI value
        # Simple approach to avoid linter errors
        try:
            rsi_value = float(rsi.iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        except:
            try:
                rsi_value = float(pd.Series(rsi).iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
            except:
                pass  # Keep default value
        
        # MACD
        macd_line = ema12 - ema26
        signal_line = macd_line.ewm(span=9).mean()  # pyright: ignore[reportAttributeAccessIssue]
        histogram = macd_line - signal_line
        macd_value = float(macd_line.iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        signal_value = float(signal_line.iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        histogram_value = float(histogram.iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        
        # Stochastic Oscillator
        low_14 = hist['Low'].rolling(window=14).min()
        high_14 = hist['High'].rolling(window=14).max()
        stoch_k = 100 * ((current_price - low_14) / (high_14 - low_14))
        stoch_d = stoch_k.rolling(window=3).mean()
        stoch_k_value = float(stoch_k.iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        stoch_d_value = float(stoch_d.iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        
        # Bollinger Bands
        bb_window = 20
        bb_std = 2
        hist['BB_MA'] = hist['Close'].rolling(window=bb_window).mean()
        hist['BB_STD'] = hist['Close'].rolling(window=bb_window).std()
        bb_upper = hist['BB_MA'] + (bb_std * hist['BB_STD'])
        bb_lower = hist['BB_MA'] - (bb_std * hist['BB_STD'])
        bb_middle = hist['BB_MA']
        bb_upper_value = float(bb_upper.iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        bb_middle_value = float(bb_middle.iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        bb_lower_value = float(bb_lower.iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        
        # Volume indicators
        current_volume = float(hist['Volume'].iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        volume_ma = float(hist['Volume'].rolling(window=20).mean().iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        
        # Status calculations
        ma20_position = 'Above' if current_price > ma20 else 'Below'
        ma50_position = 'Above' if current_price > ma50 else 'Below'
        ma200_position = 'Above' if current_price > ma200 else 'Below'
        
        rsi_status = 'Neutral'
        if rsi_value < 30:
            rsi_status = 'Oversold'
        elif rsi_value > 70:
            rsi_status = 'Overbought'
            
        macd_status = 'Neutral'
        if macd_value > signal_value:
            macd_status = 'Bullish'
        elif macd_value < signal_value:
            macd_status = 'Bearish'
            
        stoch_status = 'Neutral'
        if stoch_k_value > 80:
            stoch_status = 'Overbought'
        elif stoch_k_value < 20:
            stoch_status = 'Oversold'
            
        bb_position = 'Neutral'
        if current_price > bb_upper_value:
            bb_position = 'Above Upper Band'
        elif current_price < bb_lower_value:
            bb_position = 'Below Lower Band'
        else:
            bb_position = 'Within Bands'
            
        volume_status = 'Neutral'
        if current_volume > volume_ma:
            volume_status = 'High'
        else:
            volume_status = 'Low'
        
        return jsonify({
            'symbol': symbol,
            'price': round(current_price * 83.0, 2),
            'ma20': round(ma20 * 83.0, 2),
            'ma20_position': ma20_position,
            'ma50': round(ma50 * 83.0, 2),
            'ma50_position': ma50_position,
            'ma200': round(ma200 * 83.0, 2),
            'ma200_position': ma200_position,
            'ema12': round(ema12 * 83.0, 2),
            'ema26': round(ema26 * 83.0, 2),
            'rsi': round(rsi_value, 2),
            'rsi_status': rsi_status,
            'macd': round(macd_value, 4),
            'signal': round(signal_value, 4),
            'histogram': round(histogram_value, 4),
            'macd_status': macd_status,
            'stoch_k': round(stoch_k_value, 2),
            'stoch_d': round(stoch_d_value, 2),
            'stoch_status': stoch_status,
            'bb_upper': round(bb_upper_value * 83.0, 2),
            'bb_middle': round(bb_middle_value * 83.0, 2),
            'bb_lower': round(bb_lower_value * 83.0, 2),
            'bb_position': bb_position,
            'volume': int(current_volume),
            'volume_ma': int(volume_ma),
            'volume_status': volume_status
        })
    except Exception as e:
        print(f"Error calculating technical indicators for {symbol}: {e}")
        # Return default data in case of error
        return jsonify({
            'symbol': symbol,
            'price': 8300.00,
            'ma20': 8300.00,
            'ma20_position': 'Neutral',
            'ma50': 8300.00,
            'ma50_position': 'Neutral',
            'ma200': 8300.00,
            'ma200_position': 'Neutral',
            'ema12': 8300.00,
            'ema26': 8300.00,
            'rsi': 50.0,
            'rsi_status': 'Neutral',
            'macd': 0.0,
            'signal': 0.0,
            'histogram': 0.0,
            'macd_status': 'Neutral',
            'stoch_k': 50.0,
            'stoch_d': 50.0,
            'stoch_status': 'Neutral',
            'bb_upper': 8500.00,
            'bb_middle': 8300.00,
            'bb_lower': 8100.00,
            'bb_position': 'Neutral',
            'volume': 1000000,
            'volume_ma': 1000000,
            'volume_status': 'Neutral'
        })

@app.route('/get_news')
def get_news():
    # Generate dynamic news based on real stock movements
    articles = []
    current_date = datetime.now().strftime('%B %d, %Y')
    
    # Get top movers
    top_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META']
    movers = []
    
    for symbol in top_stocks:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period='5d')
            if len(hist) >= 2:
                current = float(hist['Close'].iloc[-1])
                previous = float(hist['Close'].iloc[-2])
                change_pct = ((current - previous) / previous) * 100
                info = stock.info
                name = info.get('shortName', symbol)
                movers.append({
                    'symbol': symbol,
                    'name': name,
                    'change': change_pct,
                    'price': current * 83.0
                })
        except:
            pass
    
    # Sort by absolute change
    movers.sort(key=lambda x: abs(x['change']), reverse=True)
    
    # Create news from top 3 movers
    if len(movers) >= 1:
        top = movers[0]
        direction = "surges" if top['change'] > 0 else "drops"
        articles.append({
            "title": f"{top['name']} {direction} {abs(top['change']):.1f}% - {current_date}",
            "summary": f"{top['name']} ({top['symbol']}) shows significant movement with {top['change']:.2f}% change. Current price: ₹{top['price']:.2f}. Market analysts monitoring closely.",
            "timestamp": datetime.now().strftime('%H:%M')
        })
    
    if len(movers) >= 2:
        second = movers[1]
        direction = "rallies" if second['change'] > 0 else "declines"
        articles.append({
            "title": f"{second['name']} {direction} {abs(second['change']):.1f}% in Latest Trading",
            "summary": f"{second['name']} experiences {abs(second['change']):.2f}% {'gain' if second['change'] > 0 else 'loss'} at ₹{second['price']:.2f}. Trading volume indicates strong investor interest.",
            "timestamp": datetime.now().strftime('%H:%M')
        })
    
    if len(movers) >= 3:
        third = movers[2]
        direction = "gains" if third['change'] > 0 else "loses"
        articles.append({
            "title": f"{third['name']} {direction} momentum as {third['symbol']} moves {abs(third['change']):.1f}%",
            "summary": f"{third['name']} continues {direction} momentum with {abs(third['change']):.2f}% movement. Current valuation at ₹{third['price']:.2f} attracts investor attention.",
            "timestamp": datetime.now().strftime('%H:%M')
        })
    
    # Add market overview
    major_indices = ['SPY', 'QQQ', 'DIA']  # S&P 500, NASDAQ, Dow Jones ETFs
    market_data = []
    total_change = 0
    
    for symbol in major_indices:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period='5d')
            if len(hist) >= 2:
                current = float(hist['Close'].iloc[-1])
                previous = float(hist['Close'].iloc[-2])
                change_pct = ((current - previous) / previous) * 100
                total_change += change_pct
                market_data.append({
                    'symbol': symbol,
                    'change': change_pct
                })
        except:
            pass
    
    # Calculate market sentiment from real data
    if market_data:
        avg_change = total_change / len(market_data)
        if avg_change > 0.5:
            market_sentiment_label = "Bullish"
        elif avg_change < -0.5:
            market_sentiment_label = "Bearish"
        else:
            market_sentiment_label = "Neutral"
        
        articles.append({
            "title": f"Market Update: {market_sentiment_label} Sentiment Prevails - {current_date}",
            "summary": f"Major indices show {market_sentiment_label.lower()} sentiment with average movement of {avg_change:.2f}%. Investors remain {market_sentiment_label.lower()} on economic outlook.",
            "timestamp": datetime.now().strftime('%H:%M')
        })
    
    # Add fallback if no articles generated
    if not articles:
        articles = [
            {
                "title": f"Market Update - {current_date}",
                "summary": "Markets are currently active. Check individual stocks for latest price movements and trading opportunities.",
                "timestamp": datetime.now().strftime('%H:%M')
            }
        ]
    
    return jsonify({
        'articles': articles,
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    # Print available routes for debugging
    with app.app_context():
        print("Available routes:")
        for rule in app.url_map.iter_rules():
            print(f"  {rule.rule} -> {rule.endpoint}")
    app.run(debug=True)