# Stock Market Trading Platform

A comprehensive web-based stock market trading platform built with Python Flask that provides real-time stock data, technical analysis, AI-powered trading signals, and portfolio management capabilities.

## Features

### 📊 Real-Time Market Data
- Live stock price tracking using Yahoo Finance API
- Interactive charts with technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands)
- Multiple time frame analysis (1D, 1W, 1M, 3M, 1Y, All)

### 🤖 AI-Powered Trading Assistant
- Machine learning-based price predictions
- Automated trading signals (BUY/SELL/HOLD) with confidence percentages
- Market sentiment analysis
- Risk assessment

### 💼 Portfolio Management
- Real-time portfolio tracking
- Performance analytics and metrics
- Transaction history
- Profit/loss calculations

### 📰 Live Market News
- Dynamic news generation based on real market movements
- Automatic updates every 5 minutes
- Company-specific news alerts

### 📈 Technical Analysis
- Professional-grade financial charts
- Customizable technical indicators
- Prediction overlays showing future price trends
- Support and resistance level detection

## Technology Stack

### Backend
- **Framework**: Python Flask
- **Data Source**: Yahoo Finance (yfinance)
- **Database**: MySQL (with mock data fallback)
- **Machine Learning**: Custom predictive models

### Frontend
- **Templates**: HTML5 with Jinja2 templating
- **Styling**: CSS3 with responsive design
- **Visualization**: Plotly.js and Chart.js
- **Interactivity**: Vanilla JavaScript

## Key Components

### Authentication System
- User registration and login
- Session-based authentication
- Secure password handling

### Market Data Engine
- Real-time stock data fetching
- Technical indicator calculation
- Chart data preparation

### Trading Engine
- Order execution (buy/sell)
- Portfolio management
- Transaction recording

### AI Analytics
- Price prediction algorithms
- Trading signal generation
- Market sentiment analysis

### News System
- Dynamic news generation
- Automatic updates every 5 minutes
- Market movement-based content

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/praveen19218/Stock-market-trading-platform-.git
   cd Stock-market-trading-platform-
   ```

2. Install required dependencies:
   ```bash
   pip install flask mysql-connector-python requests yfinance plotly
   ```

3. Run the application:
   ```bash
   python Stock_market/app.py
   ```

4. Access the application at `http://localhost:5000`

## Project Structure

```
Stock_market/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── stock_graph.html   # Main chart interface
│   ├── portfolio.html     # Portfolio management
│   ├── trade.html         # Trading interface
│   └── ...                # Other templates
├── static/                # Static assets (CSS, JS, images)
└── README.md              # This file
```

## API Endpoints

- `/stock_graph` - Interactive stock charts
- `/get_chart_data` - Real-time chart data with technical indicators
- `/get_trading_signal` - AI-powered trading signals
- `/get_news` - Live market news updates
- `/portfolio` - Portfolio management dashboard
- `/trade` - Trading interface
- `/predict_next_week` - Stock price predictions

## Academic Publications

This project has been documented in academic papers suitable for IEEE publication:
- [IEEE Paper (LaTeX)](Stock_Market_Trading_Platform_IEEE_Paper.tex)
- [IEEE Paper (PDF)](Stock_Market_Trading_Platform_IEEE_Paper.pdf)
- [Results Output (PDF)](Stock_Market_Platform_Results_Output.pdf)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is for educational and research purposes.

## Contact

For questions about this project, please contact the repository owner.