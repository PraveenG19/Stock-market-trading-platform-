from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors

def create_project_presentation_pdf():
    # Create PDF document
    output_file = r"c:\Users\S PRAVEEN KUMAR\OneDrive\Desktop\Stock_market\Stock_Market_Project_Presentation.pdf"
    doc = SimpleDocTemplate(output_file, pagesize=letter,
                          leftMargin=0.75*inch, rightMargin=0.75*inch,
                          topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        alignment=TA_CENTER,
        spaceAfter=30,
        textColor=colors.HexColor('#2563eb'),
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.HexColor('#64748b')
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=16,
        textColor=colors.HexColor('#1e293b'),
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=13,
        spaceAfter=10,
        spaceBefore=12,
        textColor=colors.HexColor('#334155'),
        fontName='Helvetica-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=11,
        spaceAfter=8,
        spaceBefore=10,
        textColor=colors.HexColor('#475569'),
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4,
        leftIndent=20,
        bulletIndent=10
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=9,
        spaceAfter=6,
        leftIndent=20,
        fontName='Courier',
        backgroundColor=colors.HexColor('#f1f5f9')
    )
    
    # Title Page
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("AI-DRIVEN STOCK MARKET", title_style))
    story.append(Paragraph("TRADING PLATFORM", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Project Presentation Guide", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("A Comprehensive Real-Time Stock Trading & Analysis System", normal_style))
    story.append(Spacer(1, 1*inch))
    
    # Technology Stack Table
    tech_data = [
        ['Component', 'Technology'],
        ['Backend Framework', 'Python Flask'],
        ['Frontend', 'HTML5, CSS3, JavaScript'],
        ['Database', 'MySQL'],
        ['Data Source', 'Yahoo Finance API (yfinance)'],
        ['Charting', 'Plotly.js, Chart.js'],
        ['Data Processing', 'Pandas, NumPy']
    ]
    
    tech_table = Table(tech_data, colWidths=[2.5*inch, 3.5*inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1'))
    ]))
    
    story.append(tech_table)
    story.append(PageBreak())
    
    # Table of Contents
    story.append(Paragraph("TABLE OF CONTENTS", heading1_style))
    story.append(Spacer(1, 0.2*inch))
    
    toc_items = [
        "1. Project Overview",
        "2. Key Features Implemented",
        "3. Technical Architecture",
        "4. UI/UX Features",
        "5. Data Flow & Integration",
        "6. Project Statistics",
        "7. Deployment & Setup",
        "8. Learning Outcomes",
        "9. Future Enhancements"
    ]
    
    for item in toc_items:
        story.append(Paragraph(item, bullet_style))
    
    story.append(PageBreak())
    
    # 1. PROJECT OVERVIEW
    story.append(Paragraph("1. PROJECT OVERVIEW", heading1_style))
    story.append(Paragraph(
        "The AI-Driven Stock Market Trading Platform is a comprehensive web-based application that enables users to track, analyze, and trade stocks in real-time. The system integrates live market data, advanced technical analysis, and AI-powered predictions to provide intelligent trading recommendations.",
        normal_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("Project Objectives:", heading2_style))
    objectives = [
        "Provide real-time stock market data with INR currency conversion",
        "Implement professional-grade charting with technical indicators",
        "Enable secure user authentication and portfolio management",
        "Integrate AI-powered price predictions and trading signals",
        "Create an intuitive, modern user interface",
        "Support multiple timeframes and analysis tools"
    ]
    for obj in objectives:
        story.append(Paragraph(f"• {obj}", bullet_style))
    
    story.append(PageBreak())
    
    # 2. KEY FEATURES IMPLEMENTED
    story.append(Paragraph("2. KEY FEATURES IMPLEMENTED", heading1_style))
    
    story.append(Paragraph("2.1 User Authentication System", heading2_style))
    features_auth = [
        "Secure login and signup functionality",
        "Session management with Flask sessions",
        "Password-protected user accounts",
        "MySQL database integration with fallback support"
    ]
    for feature in features_auth:
        story.append(Paragraph(f"• {feature}", bullet_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("2.2 Real-Time Stock Market Data", heading2_style))
    features_data = [
        "Live stock prices from Yahoo Finance API",
        "Automatic currency conversion to Indian Rupees (USD × 83.0)",
        "Support for 30+ major US stocks (AAPL, MSFT, GOOGL, TSLA, etc.)",
        "Real-time price updates and market data"
    ]
    for feature in features_data:
        story.append(Paragraph(f"• {feature}", bullet_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("2.3 Advanced Stock Chart Analysis", heading2_style))
    story.append(Paragraph("Main Price Chart:", heading3_style))
    features_chart = [
        "Multiple timeframes: 1D, 1W, 1M, 3M, 1Y, All-time",
        "Linear zig-zag chart lines for realistic stock movements",
        "Dynamic color coding (green for gains, red for losses)",
        "Horizontal price indicator showing current value",
        "Professional white background with clean styling",
        "Interactive tooltips and zoom functionality"
    ]
    for feature in features_chart:
        story.append(Paragraph(f"• {feature}", bullet_style))
    
    story.append(Paragraph("High/Low Price Charts:", heading3_style))
    features_highlow = [
        "Separate dedicated charts for daily high and low prices",
        "Green area chart for high prices",
        "Red area chart for low prices",
        "Synchronized with main chart timeframe",
        "Real-time data visualization"
    ]
    for feature in features_highlow:
        story.append(Paragraph(f"• {feature}", bullet_style))
    
    story.append(Paragraph("Technical Indicators:", heading3_style))
    features_indicators = [
        "Moving Averages: SMA 20, SMA 50, SMA 200, EMA 12, EMA 26",
        "Momentum Indicators: RSI (14), MACD, Stochastic Oscillator (%K, %D)",
        "Volatility Indicators: Bollinger Bands (Upper, Middle, Lower)",
        "Volume Indicators: Current Volume, Volume MA (20)",
        "Color-coded buy/sell signals",
        "Real-time indicator calculations"
    ]
    for feature in features_indicators:
        story.append(Paragraph(f"• {feature}", bullet_style))
    
    story.append(PageBreak())
    
    story.append(Paragraph("2.4 Portfolio Management", heading2_style))
    features_portfolio = [
        "Track owned stocks with quantity and average price",
        "Real-time portfolio value calculation",
        "Profit/loss tracking for each position",
        "Total portfolio performance metrics",
        "Visual profit/loss indicators"
    ]
    for feature in features_portfolio:
        story.append(Paragraph(f"• {feature}", bullet_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("2.5 Trading Functionality", heading2_style))
    features_trading = [
        "Buy and sell stocks at real-time prices",
        "Transaction validation and confirmation",
        "Balance management and tracking",
        "Order execution with current market prices",
        "Transaction history logging"
    ]
    for feature in features_trading:
        story.append(Paragraph(f"• {feature}", bullet_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("2.6 AI-Powered Predictions", heading2_style))
    features_ai = [
        "1-day price prediction based on historical trends",
        "7-day forecast charts with visual comparison",
        "Buy/Sell/Hold recommendations",
        "RSI-based technical analysis",
        "Historical vs. predicted price visualization",
        "Confidence indicators for predictions"
    ]
    for feature in features_ai:
        story.append(Paragraph(f"• {feature}", bullet_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("2.7 Market Sentiment Analysis", heading2_style))
    features_sentiment = [
        "Overall market sentiment scoring (Bullish/Bearish/Neutral)",
        "Sector-wise sentiment analysis",
        "News integration and display",
        "Sentiment indicators with visual representation"
    ]
    for feature in features_sentiment:
        story.append(Paragraph(f"• {feature}", bullet_style))
    
    story.append(PageBreak())
    
    # 3. TECHNICAL ARCHITECTURE
    story.append(Paragraph("3. TECHNICAL ARCHITECTURE", heading1_style))
    
    story.append(Paragraph("3.1 Backend Structure (Flask)", heading2_style))
    story.append(Paragraph("app.py - Main Application (1,300+ lines)", heading3_style))
    
    backend_structure = [
        "Authentication Routes: /login, /signup, /logout",
        "Dashboard Routes: /, /portfolio, /trade, /trading_history",
        "Chart Routes: /stock_graph, /prediction_chart",
        "Analysis Routes: /sentiment_analysis",
        "API Endpoints:",
        "  - /get_chart_data: Stock price data with high/low values",
        "  - /get_stock_data: Real-time stock information",
        "  - /get_1d_prediction: AI-powered price predictions",
        "  - /get_technical_indicators: RSI, MACD, Bollinger Bands",
        "  - /get_multiple_stock_data: Batch stock data retrieval",
        "  - /get_trading_signal: Buy/Sell/Hold recommendations",
        "Database Integration: MySQL with automatic fallback",
        "Session Management: Secure user sessions",
        "Error Handling: Comprehensive exception handling with fallbacks"
    ]
    for item in backend_structure:
        story.append(Paragraph(f"• {item}", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("3.2 Frontend Templates", heading2_style))
    
    templates = [
        "login.html (15.3KB) - Authentication with AI-themed animated background",
        "signup.html (6.8KB) - User registration",
        "home.html (25.2KB) - Main dashboard with market overview",
        "stock_graph.html (76.4KB) - Advanced charting interface (most complex)",
        "trade.html (79.4KB) - Trading interface with real-time execution",
        "portfolio.html (17.8KB) - Portfolio management dashboard",
        "prediction_chart.html (25.8KB) - AI prediction visualization",
        "sentiment_analysis.html (18.0KB) - Market sentiment analysis",
        "trading_history.html (10.2KB) - Transaction history log"
    ]
    for template in templates:
        story.append(Paragraph(f"• {template}", bullet_style))
    
    story.append(PageBreak())
    
    # 4. UI/UX FEATURES
    story.append(Paragraph("4. UI/UX FEATURES", heading1_style))
    
    story.append(Paragraph("4.1 AI-Themed Design Elements", heading2_style))
    ui_ai = [
        "Animated background charts with real-time data",
        "Pulse circles and grid lines for depth effect",
        "Glass-morphism effects on UI cards",
        "Modern dark theme (#0f172a) with blue accents (#60a5fa)",
        "Smooth transitions and animations",
        "Responsive design for all screen sizes"
    ]
    for item in ui_ai:
        story.append(Paragraph(f"• {item}", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("4.2 Professional Dashboard Features", heading2_style))
    ui_dashboard = [
        "Clean, minimalist interface design",
        "Intuitive navigation with clear sections",
        "Real-time data updates without page refresh",
        "Color-coded indicators (green/red for gains/losses)",
        "Interactive charts with zoom and pan",
        "Tooltip information on hover",
        "Mobile-friendly responsive layout"
    ]
    for item in ui_dashboard:
        story.append(Paragraph(f"• {item}", bullet_style))
    
    story.append(PageBreak())
    
    # 5. DATA FLOW & INTEGRATION
    story.append(Paragraph("5. DATA FLOW & INTEGRATION", heading1_style))
    
    story.append(Paragraph("Data Processing Pipeline:", heading2_style))
    story.append(Paragraph("1. User Request → Flask Route Handler", normal_style))
    story.append(Paragraph("2. Flask Route → yfinance API Call", normal_style))
    story.append(Paragraph("3. Yahoo Finance → Raw Stock Data (USD)", normal_style))
    story.append(Paragraph("4. Data Processing → INR Conversion (× 83.0)", normal_style))
    story.append(Paragraph("5. Technical Indicators → RSI, MACD, MA calculations", normal_style))
    story.append(Paragraph("6. JSON Response → JavaScript Frontend", normal_style))
    story.append(Paragraph("7. Chart.js/Plotly → Visual Rendering", normal_style))
    story.append(Paragraph("8. DOM Update → User Display", normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("API Integration Details:", heading2_style))
    api_details = [
        "yfinance library for Yahoo Finance data access",
        "Pandas for data manipulation and analysis",
        "NumPy for numerical calculations",
        "Real-time price fetching with multiple fallback periods",
        "Automatic error handling and data validation",
        "Caching mechanisms for improved performance"
    ]
    for detail in api_details:
        story.append(Paragraph(f"• {detail}", bullet_style))
    
    story.append(PageBreak())
    
    # 6. PROJECT STATISTICS
    story.append(Paragraph("6. PROJECT STATISTICS", heading1_style))
    
    stats_data = [
        ['Metric', 'Value'],
        ['Total Backend Code', '1,300+ lines (Python)'],
        ['Total Frontend Code', '~400KB (HTML/CSS/JS)'],
        ['Number of Templates', '17 HTML pages'],
        ['API Endpoints', '15+ routes'],
        ['Supported Stocks', '30+ major US stocks'],
        ['Technical Indicators', '15+ metrics'],
        ['Chart Types', '3 (Main, High, Low)'],
        ['Timeframes Supported', '6 periods (1D to All-time)'],
        ['Database Tables', '3 (users, portfolio, history)'],
        ['External APIs', '1 (Yahoo Finance)'],
        ['Chart Libraries', '2 (Plotly.js, Chart.js)']
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fdf4')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#86efac'))
    ]))
    
    story.append(stats_table)
    
    story.append(PageBreak())
    
    # 7. DEPLOYMENT & SETUP
    story.append(Paragraph("7. DEPLOYMENT & SETUP", heading1_style))
    
    story.append(Paragraph("7.1 Installation Requirements", heading2_style))
    story.append(Paragraph("Install required Python packages:", normal_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("pip install flask mysql-connector-python yfinance pandas plotly", code_style))
    
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("7.2 Database Setup (Optional)", heading2_style))
    db_setup = [
        "MySQL Server installation (localhost)",
        "Database name: stock_trading",
        "Required tables: users, portfolio, trading_history",
        "Automatic fallback to in-memory storage if MySQL unavailable"
    ]
    for item in db_setup:
        story.append(Paragraph(f"• {item}", bullet_style))
    
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("7.3 Running the Application", heading2_style))
    story.append(Paragraph("Execute the following command:", normal_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph('python "c:\\Users\\S PRAVEEN KUMAR\\OneDrive\\Desktop\\Stock_market\\Stock_market\\app.py"', code_style))
    
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("7.4 Access the Application", heading2_style))
    story.append(Paragraph("Open your web browser and navigate to:", normal_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("http://127.0.0.1:5000", code_style))
    
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("7.5 Development Mode Features", heading2_style))
    dev_features = [
        "Debug mode enabled for automatic reload on code changes",
        "Detailed error messages for troubleshooting",
        "Console logging for request/response tracking",
        "No caching for immediate updates during development"
    ]
    for feature in dev_features:
        story.append(Paragraph(f"• {feature}", bullet_style))
    
    story.append(PageBreak())
    
    # 8. LEARNING OUTCOMES
    story.append(Paragraph("8. LEARNING OUTCOMES", heading1_style))
    
    learning_outcomes = [
        ("Full-Stack Web Development", "Integrated Flask backend with modern HTML/CSS/JS frontend, managing both server-side and client-side logic"),
        ("RESTful API Design", "Created and consumed RESTful APIs for data exchange between frontend and backend"),
        ("External API Integration", "Integrated Yahoo Finance API for real-time stock market data"),
        ("Data Visualization", "Implemented advanced charting with Plotly.js and Chart.js for interactive data display"),
        ("Financial Analysis", "Applied technical indicators (RSI, MACD, Bollinger Bands) and trading logic"),
        ("Database Management", "Designed and implemented MySQL database schema with CRUD operations"),
        ("User Authentication", "Implemented secure session-based authentication and authorization"),
        ("UI/UX Design", "Created professional, responsive user interfaces with modern design principles"),
        ("State Management", "Managed application state using Flask sessions and client-side JavaScript"),
        ("Error Handling", "Implemented comprehensive error handling with fallback mechanisms"),
        ("Data Processing", "Used Pandas and NumPy for efficient data manipulation and analysis"),
        ("Asynchronous Operations", "Handled real-time data updates without blocking the user interface")
    ]
    
    for outcome, description in learning_outcomes:
        story.append(Paragraph(f"<b>{outcome}:</b> {description}", normal_style))
        story.append(Spacer(1, 0.05*inch))
    
    story.append(PageBreak())
    
    # 9. FUTURE ENHANCEMENTS
    story.append(Paragraph("9. FUTURE ENHANCEMENTS", heading1_style))
    
    story.append(Paragraph("9.1 Machine Learning Integration", heading2_style))
    ml_enhancements = [
        "LSTM neural networks for price prediction",
        "Sentiment analysis using NLP on news articles",
        "Pattern recognition for chart analysis",
        "Anomaly detection for market events",
        "Portfolio optimization using reinforcement learning"
    ]
    for item in ml_enhancements:
        story.append(Paragraph(f"• {item}", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("9.2 Real-Time Features", heading2_style))
    realtime_enhancements = [
        "WebSocket integration for live price streaming",
        "Real-time notifications for price alerts",
        "Live order book visualization",
        "Multi-user chat for trading discussions",
        "Real-time portfolio updates across devices"
    ]
    for item in realtime_enhancements:
        story.append(Paragraph(f"• {item}", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("9.3 Platform Extensions", heading2_style))
    platform_enhancements = [
        "Mobile application (React Native/Flutter)",
        "Desktop application (Electron)",
        "Multi-currency support (USD, EUR, GBP, JPY)",
        "Multiple stock exchanges (NYSE, NASDAQ, BSE, NSE)",
        "Cryptocurrency trading integration",
        "Forex market support"
    ]
    for item in platform_enhancements:
        story.append(Paragraph(f"• {item}", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("9.4 Advanced Features", heading2_style))
    advanced_enhancements = [
        "Social trading and copy trading features",
        "Advanced portfolio analytics and risk metrics",
        "Automated trading bots with custom strategies",
        "Backtesting framework for strategy validation",
        "Options and derivatives trading",
        "News sentiment analysis with NLP",
        "Customizable alerts and notifications",
        "API access for third-party integrations"
    ]
    for item in advanced_enhancements:
        story.append(Paragraph(f"• {item}", bullet_style))
    
    story.append(PageBreak())
    
    # DEMO GUIDE
    story.append(Paragraph("10. DEMONSTRATION GUIDE", heading1_style))
    
    story.append(Paragraph("Follow these steps for an effective project demonstration:", normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    demo_steps = [
        ("Step 1: Login Page", "Showcase the AI-themed animated background with moving charts and pulse effects. Demonstrate the login functionality."),
        ("Step 2: Dashboard Overview", "Navigate to the main dashboard. Point out real-time stock prices, market indices, and portfolio summary."),
        ("Step 3: Stock Chart Analysis", "Open the stock graph page. Demonstrate timeframe switching (1D, 1W, 1M, etc.) and show how the chart updates."),
        ("Step 4: High/Low Charts", "Highlight the dedicated high and low price charts below the main chart. Explain the color coding."),
        ("Step 5: Technical Indicators", "Scroll through the technical indicators panel. Explain RSI, MACD, and Bollinger Bands."),
        ("Step 6: Stock Selection", "Change the stock symbol from the dropdown. Show how all charts and data update automatically."),
        ("Step 7: Trading Execution", "Navigate to the trade page. Execute a sample buy or sell order with real-time price."),
        ("Step 8: Portfolio View", "Open portfolio page. Display holdings, current value, and profit/loss calculations."),
        ("Step 9: AI Predictions", "Show the prediction chart page with 7-day forecast. Explain the buy/sell recommendations."),
        ("Step 10: Transaction History", "Review the trading history page showing all executed trades with timestamps and prices.")
    ]
    
    for step, description in demo_steps:
        story.append(Paragraph(f"<b>{step}:</b>", heading3_style))
        story.append(Paragraph(description, normal_style))
        story.append(Spacer(1, 0.08*inch))
    
    story.append(PageBreak())
    
    # CONCLUSION
    story.append(Paragraph("CONCLUSION", heading1_style))
    story.append(Paragraph(
        "The AI-Driven Stock Market Trading Platform represents a comprehensive solution for modern stock trading and analysis. "
        "By integrating real-time market data, advanced technical analysis, and AI-powered predictions, the platform provides "
        "users with professional-grade tools for making informed trading decisions.",
        normal_style
    ))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "The project demonstrates proficiency in full-stack web development, API integration, data visualization, and financial "
        "analysis. The modular architecture and clean code structure ensure maintainability and scalability for future enhancements.",
        normal_style
    ))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "With a solid foundation in place, the platform is well-positioned for expansion into mobile applications, machine learning "
        "integration, and support for additional financial instruments and markets.",
        normal_style
    ))
    
    # Build PDF
    doc.build(story)
    print(f"\n✅ PDF created successfully!")
    print(f"📄 Location: {output_file}")
    print(f"📊 Total pages: Multiple pages with comprehensive documentation")

if __name__ == "__main__":
    create_project_presentation_pdf()
