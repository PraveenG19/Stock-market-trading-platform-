import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime

def create_execution_steps_pdf():
    """
    Generate a PDF with execution steps and explanation for the Stock Market Trading Platform
    """
    
    # Create PDF document
    doc = SimpleDocTemplate("Stock_Market_Execution_Steps.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Center alignment
        leading=22,
        textColor=colors.HexColor("#2563eb")
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        spaceBefore=25,
        textColor=colors.HexColor("#3b82f6")
    )
    
    author_style = ParagraphStyle(
        'AuthorStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1,  # Center alignment
        spaceAfter=30
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.HexColor("#1d4ed8")
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=10,
        spaceBefore=15,
        textColor=colors.HexColor("#2563eb")
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=6,
        fontName='Courier',
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=1,
        borderPadding=10,
        borderRadius=5
    )
    
    # Build content
    story = []
    
    # Title
    story.append(Paragraph("Stock Market Trading Platform", title_style))
    story.append(Paragraph("Execution Steps and Explanation", styles['Heading2']))
    story.append(Spacer(1, 20))
    
    # 1. Prerequisites
    story.append(Paragraph("1. Prerequisites", heading1_style))
    story.append(Paragraph("Before running the application, ensure you have:", normal_style))
    
    prerequisites = [
        "Python 3.7 or higher installed",
        "Internet connection (for fetching real stock data)",
        "Git (optional, for cloning the repository)"
    ]
    
    prereq_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in prerequisites],
        bulletType='bullet'
    )
    story.append(prereq_list)
    
    # 2. Step-by-Step Execution Guide
    story.append(PageBreak())
    story.append(Paragraph("2. Step-by-Step Execution Guide", heading1_style))
    
    # Step 1: Clone or Download
    story.append(Paragraph("Step 1: Clone or Download the Repository", heading2_style))
    story.append(Paragraph("""
    Clone the repository using Git:
    """, normal_style))
    story.append(Paragraph("""
    git clone https://github.com/praveen19218/Stock-market-trading-platform-.git
    cd Stock-market-trading-platform-
    """, code_style))
    
    story.append(Paragraph("Or download the ZIP file from GitHub and extract it.", normal_style))
    
    # Step 2: Navigate to Project Directory
    story.append(Paragraph("Step 2: Navigate to the Project Directory", heading2_style))
    story.append(Paragraph("""
    Change to the Stock_market directory:
    """, normal_style))
    story.append(Paragraph("""
    cd Stock_market
    """, code_style))
    
    # Step 3: Install Dependencies
    story.append(Paragraph("Step 3: Install Required Dependencies", heading2_style))
    story.append(Paragraph("""
    The application requires several Python packages. Install them using pip:
    """, normal_style))
    story.append(Paragraph("""
    pip install flask mysql-connector-python requests yfinance plotly pandas numpy
    """, code_style))
    
    story.append(Paragraph("Explanation of Dependencies:", subtitle_style))
    deps = [
        "Flask: Web framework for building the application",
        "mysql-connector-python: Database connector for MySQL",
        "requests: HTTP library for API calls",
        "yfinance: Yahoo Finance API wrapper for stock data",
        "plotly: Interactive charting library",
        "pandas: Data manipulation library",
        "numpy: Numerical computing library"
    ]
    
    deps_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in deps],
        bulletType='bullet'
    )
    story.append(deps_list)
    
    # Step 4: Run the Application
    story.append(PageBreak())
    story.append(Paragraph("Step 4: Run the Application", heading2_style))
    story.append(Paragraph("""
    Execute the main application file:
    """, normal_style))
    story.append(Paragraph("""
    python app.py
    """, code_style))
    
    story.append(Paragraph("Expected Output:", subtitle_style))
    story.append(Paragraph("""
    * Running on http://127.0.0.1:5000
    * Debug mode: on
    """, code_style))
    
    # Step 5: Access the Application
    story.append(Paragraph("Step 5: Access the Application", heading2_style))
    story.append(Paragraph("""
    Open your web browser and navigate to:
    """, normal_style))
    story.append(Paragraph("""
    http://localhost:5000
    """, code_style))
    
    # 3. Application Structure and Components
    story.append(PageBreak())
    story.append(Paragraph("3. Application Structure and Components", heading1_style))
    
    # Main Application File
    story.append(Paragraph("Main Application File (app.py)", heading2_style))
    story.append(Paragraph("This is the core of the application containing:", normal_style))
    
    main_components = [
        "Flask Setup for web framework configuration",
        "Routes for different application functionalities",
        "Mock Data Structures for simulated user data",
        "Integration with Yahoo Finance API for real-time data"
    ]
    
    components_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in main_components],
        bulletType='bullet'
    )
    story.append(components_list)
    
    # Key Routes
    story.append(Paragraph("Key Routes:", subtitle_style))
    routes = [
        "/login and /signup for user authentication",
        "/stock_graph for interactive stock charts",
        "/portfolio for portfolio management",
        "/trade for buying/selling stocks",
        "/get_chart_data for real-time chart data",
        "/get_trading_signal for AI-powered trading signals",
        "/get_news for live market news"
    ]
    
    routes_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in routes],
        bulletType='bullet'
    )
    story.append(routes_list)
    
    # Mock Data Structures
    story.append(Paragraph("Mock Data Structures:", subtitle_style))
    mock_data = [
        "MOCK_USERS: Simulated user accounts",
        "MOCK_PORTFOLIO: Sample portfolio data",
        "MOCK_TRADING_HISTORY: Example trading history"
    ]
    
    mock_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in mock_data],
        bulletType='bullet'
    )
    story.append(mock_list)
    
    # 4. Key Features Explained
    story.append(PageBreak())
    story.append(Paragraph("4. Key Features Explained", heading1_style))
    
    # Real-Time Stock Charts
    story.append(Paragraph("1. Real-Time Stock Charts (/stock_graph)", heading2_style))
    chart_features = [
        "Displays interactive charts using Plotly.js",
        "Shows technical indicators (SMA, EMA, RSI, MACD)",
        "Supports multiple time frames (1D, 1W, 1M, etc.)",
        "Fetches real data from Yahoo Finance via yfinance"
    ]
    
    chart_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in chart_features],
        bulletType='bullet'
    )
    story.append(chart_list)
    
    # AI-Powered Trading Signals
    story.append(Paragraph("2. AI-Powered Trading Signals (/get_trading_signal)", heading2_style))
    signal_features = [
        "Analyzes stock trends using moving averages",
        "Generates BUY/SELL/HOLD recommendations",
        "Provides confidence metrics",
        "Uses technical analysis for decision making"
    ]
    
    signal_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in signal_features],
        bulletType='bullet'
    )
    story.append(signal_list)
    
    # Live News Updates
    story.append(Paragraph("3. Live News Updates (/get_news)", heading2_style))
    news_features = [
        "Automatically refreshes every 5 minutes",
        "Generates news based on real market movements",
        "Shows top gainers/losers",
        "Provides market sentiment analysis"
    ]
    
    news_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in news_features],
        bulletType='bullet'
    )
    story.append(news_list)
    
    # Portfolio Management
    story.append(Paragraph("4. Portfolio Management (/portfolio)", heading2_style))
    portfolio_features = [
        "Tracks holdings and performance",
        "Calculates profit/loss in real-time",
        "Shows sector allocation",
        "Displays transaction history"
    ]
    
    portfolio_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in portfolio_features],
        bulletType='bullet'
    )
    story.append(portfolio_list)
    
    # 5. Database Configuration
    story.append(PageBreak())
    story.append(Paragraph("5. Database Configuration (Optional)", heading1_style))
    story.append(Paragraph("The application uses mock data by default but can connect to a MySQL database:", normal_style))
    
    db_steps = [
        "Install MySQL Server (if not already installed)",
        "Create Database: CREATE DATABASE stock_trading;",
        "Update Connection Details in app.py"
    ]
    
    db_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in db_steps],
        bulletType='bullet'
    )
    story.append(db_list)
    
    story.append(Paragraph("Connection Code Example:", subtitle_style))
    story.append(Paragraph("""
    conn = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='stock_trading'
    )
    """, code_style))
    
    # 6. Troubleshooting
    story.append(PageBreak())
    story.append(Paragraph("6. Troubleshooting Common Issues", heading1_style))
    
    issues = [
        "Port Already in Use: python app.py --port 5001",
        "Missing Dependencies: pip install -r requirements.txt",
        "yfinance API Issues: Check internet connection or update yfinance",
        "Permission Errors: Run as administrator or adjust firewall settings"
    ]
    
    issues_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in issues],
        bulletType='bullet'
    )
    story.append(issues_list)
    
    # 7. Testing the Application
    story.append(Paragraph("7. Testing the Application", heading1_style))
    story.append(Paragraph("Login with mock credentials:", normal_style))
    
    login_creds = [
        "Username: admin",
        "Password: admin123"
    ]
    
    creds_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in login_creds],
        bulletType='bullet'
    )
    story.append(creds_list)
    
    story.append(Paragraph("Explore Features:", normal_style))
    features = [
        "View stock charts for AAPL, MSFT, GOOGL",
        "Check AI trading signals",
        "Browse portfolio dashboard",
        "View trading history",
        "See live news updates"
    ]
    
    features_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in features],
        bulletType='bullet'
    )
    story.append(features_list)
    
    # 8. Stopping the Application
    story.append(Paragraph("8. Stopping the Application", heading1_style))
    story.append(Paragraph("To stop the application, press Ctrl+C in the terminal where it's running.", normal_style))
    
    # 9. Customization Options
    story.append(Paragraph("9. Customization Options", heading1_style))
    custom_options = [
        "Adding New Stocks: Modify stock symbols in various routes",
        "Adjusting Time Frames: Edit period mappings in /get_chart_data route",
        "Modifying Technical Indicators: Update calculation logic in chart data functions"
    ]
    
    custom_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in custom_options],
        bulletType='bullet'
    )
    story.append(custom_list)
    
    # Conclusion
    story.append(PageBreak())
    story.append(Paragraph("Conclusion", heading1_style))
    story.append(Paragraph("""
    This comprehensive guide should help you successfully execute and understand the Stock Market Trading Platform code. 
    The application demonstrates real-world implementation of financial technology with modern web development practices.
    """, normal_style))
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey)))
    
    # Build PDF
    try:
        doc.build(story)
        print("Execution steps PDF generated successfully: Stock_Market_Execution_Steps.pdf")
        return True
    except Exception as e:
        print(f"Error generating execution steps PDF: {e}")
        return False

if __name__ == "__main__":
    create_execution_steps_pdf()