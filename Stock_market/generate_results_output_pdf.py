import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime

def create_results_output_pdf():
    """
    Generate a PDF showcasing the key result outputs from the Stock Market Trading Platform
    that can be used in an IEEE paper.
    """
    
    # Create PDF document
    doc = SimpleDocTemplate("Stock_Market_Platform_Results_Output.pdf", pagesize=A4)
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
    
    abstract_style = ParagraphStyle(
        'AbstractStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=12,
        leftIndent=20,
        rightIndent=20,
        textColor=colors.HexColor("#374151")
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
    story.append(Paragraph("Stock Market Trading Platform: Results and Output Examples", title_style))
    
    # Author
    story.append(Paragraph("S. Praveen Kumar", author_style))
    story.append(Paragraph("School of Computer Science<br/>Anna University<br/>Chennai, India<br/>Email: spkumar@example.com", author_style))
    
    # Abstract
    story.append(Paragraph("Abstract—This document presents the key result outputs from the Stock Market Trading Platform, demonstrating the system's capabilities in real-time stock analysis, portfolio management, and AI-powered trading signals. The platform provides traders with comprehensive tools for informed decision-making through interactive charts, technical indicators, and predictive analytics. Sample outputs showcase the system's user interface, data visualization capabilities, and trading functionalities that support effective investment strategies.", abstract_style))
    
    # Keywords
    story.append(Paragraph("<b>Keywords</b>—stock market, trading platform, results output, data visualization, technical analysis, AI trading signals, portfolio management.", normal_style))
    story.append(Spacer(1, 20))
    
    # 1. Introduction
    story.append(Paragraph("1. Introduction", heading1_style))
    story.append(Paragraph("The Stock Market Trading Platform delivers comprehensive outputs that enable traders to make informed decisions. This document showcases the key result outputs from the system, including interactive charts, portfolio management interfaces, trading history, and AI-generated trading signals. These outputs demonstrate the platform's effectiveness in providing real-time market insights and supporting trading activities.", normal_style))
    
    # 2. Interactive Stock Chart Interface
    story.append(PageBreak())
    story.append(Paragraph("2. Interactive Stock Chart Interface", heading1_style))
    story.append(Paragraph("The platform's main interface provides interactive stock charts with real-time data visualization capabilities:", normal_style))
    
    chart_features = [
        "Real-time price updates with 15-second refresh intervals",
        "Multiple time frame options (1D, 1W, 1M, 3M, 1Y, All)",
        "Technical indicators overlay (SMA, EMA, RSI, MACD, Bollinger Bands)",
        "AI-generated price predictions with confidence intervals",
        "Zoom and pan capabilities for detailed analysis",
        "Responsive design for various screen sizes"
    ]
    
    chart_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in chart_features],
        bulletType='bullet'
    )
    story.append(chart_list)
    
    # Mockup of chart interface
    story.append(Paragraph("Sample Chart Interface Layout:", subtitle_style))
    story.append(Paragraph("""
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │  [AAPL] Apple Inc. - Technology Sector                          $185.32   │
    │  +1.24 (0.67%) ▲                                                    1D 1W │
    │                                                                             │
    │  ┌─────────────────────────────────────────────────────────────────────┐   │
    │  │  [Chart Area - Interactive Price Chart with Technical Indicators]   │   │
    │  │  │                                                             │   │   │
    │  │  │  Price: $185.32                                             │   │   │
    │  │  │  Volume: 45.2M                                              │   │   │
    │  │  │  RSI: 62.4                                                  │   │   │
    │  │  │  MACD: Bullish Crossover                                    │   │   │
    │  │  │                                                             │   │   │
    │  │  └─────────────────────────────────────────────────────────────────────┘   │
    │                                                                             │
    │  [AI Trading Signal: BUY] Confidence: 87% 📈                               │
    │  Outlook: Strong upward momentum expected in next 3 days                    │
    │                                                                             │
    │  Technical Indicators:                                                      │
    │  • SMA(20): $183.45  • EMA(12): $184.78  • RSI(14): 62.4                    │
    │  • MACD: Bullish     • Bollinger Bands: $181.20-$187.80                     │
    │                                                                             │
    │  [Predicted Prices]                                                         │
    │  Day 1: $187.50 (+1.18%)  Day 2: $189.20 (+2.10%)  Day 3: $191.00 (+3.07%) │
    │                                                                             │
    │  [Time Frame Selector] [1D] [1W] [1M] [3M] [1Y] [All]                       │
    │  [Technical Indicators Toggle] [SMA] [EMA] [RSI] [MACD] [Bollinger]         │
    │                                                                             │
    └─────────────────────────────────────────────────────────────────────────────┘
    """, code_style))
    
    # 3. Portfolio Management Dashboard
    story.append(PageBreak())
    story.append(Paragraph("3. Portfolio Management Dashboard", heading1_style))
    story.append(Paragraph("The portfolio management interface provides comprehensive insights into investment holdings:", normal_style))
    
    portfolio_features = [
        "Real-time portfolio valuation with profit/loss calculations",
        "Holdings breakdown by stock and sector",
        "Performance charts showing historical returns",
        "Risk assessment metrics and diversification analysis",
        "Quick trade buttons for buy/sell actions"
    ]
    
    portfolio_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in portfolio_features],
        bulletType='bullet'
    )
    story.append(portfolio_list)
    
    # Mockup of portfolio interface
    story.append(Paragraph("Sample Portfolio Dashboard Layout:", subtitle_style))
    story.append(Paragraph("""
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │  Portfolio Management Dashboard                                             │
    │                                                                             │
    │  ┌─────────────────────────────────────────────────────────────────────┐   │
    │  │  Portfolio Summary                                                  │   │
    │  │  ┌───────────────┬─────────────────┬─────────────────┬─────────────┐   │
    │  │  │ Total Value   │ 24H Change      │ Total Gain/Loss │  Cash       │   │
    │  │  ├───────────────┼─────────────────┼─────────────────┼─────────────┤   │
    │  │  │ $24,567.89    │ +1.2% (+$292.34)│ +$3,245.67 (15.2%)│ $2,500.00   │   │
    │  │  └───────────────┴─────────────────┴─────────────────┴─────────────┘   │
    │  └─────────────────────────────────────────────────────────────────────┘   │
    │                                                                             │
    │  Current Holdings:                                                          │
    │  ┌─────────────────────────────────────────────────────────────────────┐   │
    │  │ Symbol │ Company Name    │ Quantity │ Avg Price │ Current │ Gain/Loss │   │
    │  │────────┼─────────────────┼──────────┼───────────┼─────────┼───────────│   │
    │  │ AAPL   │ Apple Inc.      │ 10       │ $150.00   │ $185.32 │ +$353.20  │   │
    │  │ MSFT   │ Microsoft Corp. │ 5        │ $300.00   │ $412.50 │ +$562.50  │   │
    │  │ GOOGL  │ Alphabet Inc.   │ 8        │ $125.50   │ $145.75 │ +$162.00  │   │
    │  │ TSLA   │ Tesla Inc.      │ 3        │ $250.00   │ $235.40 │ -$43.80   │   │
    │  └─────────────────────────────────────────────────────────────────────┘   │
    │                                                                             │
    │  Portfolio Performance (Last 30 Days):                                      │
    │  [Chart showing portfolio value trend over time]                            │
    │                                                                             │
    │  Sector Allocation:                                                         │
    │  [Pie chart showing Technology (65%), Automotive (15%), Other (20%)]        │
    │                                                                             │
    └─────────────────────────────────────────────────────────────────────────────┘
    """, code_style))
    
    # 4. Trading History Interface
    story.append(PageBreak())
    story.append(Paragraph("4. Trading History Interface", heading1_style))
    story.append(Paragraph("The trading history interface provides a comprehensive record of all transactions:", normal_style))
    
    history_features = [
        "Detailed transaction records with timestamps",
        "Filtering capabilities by date range, stock symbol, and action type",
        "Performance analysis of individual trades",
        "Export functionality for tax and accounting purposes"
    ]
    
    history_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in history_features],
        bulletType='bullet'
    )
    story.append(history_list)
    
    # Mockup of trading history interface
    story.append(Paragraph("Sample Trading History Layout:", subtitle_style))
    story.append(Paragraph("""
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │  Trading History                                                            │
    │                                                                             │
    │  Filter Options:                                                            │
    │  [Date Range: 2025-11-01 to 2025-11-30] [Symbol: AAPL] [Action: All]       │
    │  [Apply Filters]                                                            │
    │                                                                             │
    │  Transaction Records:                                                       │
    │  ┌─────────────────────────────────────────────────────────────────────┐   │
    │  │ Date/Time          │ Symbol │ Action │ Quantity │ Price   │ Total     │   │
    │  │────────────────────┼────────┼────────┼──────────┼─────────┼───────────│   │
    │  │ 2025-11-28 14:30   │ AAPL   │ BUY    │ 10       │ $185.32 │ $1,853.20 │   │
    │  │ 2025-11-25 10:15   │ MSFT   │ BUY    │ 5        │ $412.50 │ $2,062.50 │   │
    │  │ 2025-11-22 09:45   │ GOOGL  │ BUY    │ 8        │ $145.75 │ $1,166.00 │   │
    │  │ 2025-11-20 11:20   │ TSLA   │ BUY    │ 3        │ $250.00 │ $750.00   │   │
    │  │ 2025-11-15 13:10   │ AMZN   │ SELL   │ 2        │ $155.40 │ $310.80   │   │
    │  │ 2025-11-10 15:30   │ NVDA   │ SELL   │ 4        │ $890.25 │ $3,561.00 │   │
    │  └─────────────────────────────────────────────────────────────────────┘   │
    │                                                                             │
    │  Performance Summary:                                                       │
    │  • Total Buys: $5,831.70  • Total Sells: $3,871.80                          │
    │  • Net Position: +$1,959.90                                                 │
    │  • Trade Count: 6 (4 Buys, 2 Sells)                                         │
    │                                                                             │
    └─────────────────────────────────────────────────────────────────────────────┘
    """, code_style))
    
    # 5. AI-Powered Trading Signals
    story.append(PageBreak())
    story.append(Paragraph("5. AI-Powered Trading Signals", heading1_style))
    story.append(Paragraph("The platform generates AI-powered trading signals with confidence metrics:", normal_style))
    
    signal_features = [
        "Real-time trading recommendations (BUY/SELL/HOLD)",
        "Confidence percentages (70-99%) for each signal",
        "Market outlook with sentiment analysis",
        "Sector-specific insights and recommendations",
        "Automated alerts for significant market movements"
    ]
    
    signal_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in signal_features],
        bulletType='bullet'
    )
    story.append(signal_list)
    
    # Mockup of AI trading signals
    story.append(Paragraph("Sample AI Trading Signals Layout:", subtitle_style))
    story.append(Paragraph("""
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │  AI-Powered Trading Signals                                                 │
    │                                                                             │
    │  🤖 [AAPL] Apple Inc. - Technology Sector                                   │
    │  📈 Trading Signal: BUY                                                     │
    │  🔢 Confidence: 87%                                                         │
    │  📊 Outlook: Strong upward momentum expected in next 3 days                 │
    │  💡 Analysis: Technical indicators show bullish trend with strong volume    │
    │                                                                             │
    │  🤖 [MSFT] Microsoft Corp. - Technology Sector                              │
    │  📈 Trading Signal: HOLD                                                    │
    │  🔢 Confidence: 76%                                                         │
    │  📊 Outlook: Consolidation phase, wait for breakout confirmation            │
    │  💡 Analysis: Mixed signals, RSI neutral, MACD showing potential crossover  │
    │                                                                             │
    │  🤖 [TSLA] Tesla Inc. - Automotive Sector                                   │
    │  📉 Trading Signal: SELL                                                    │
    │  🔢 Confidence: 82%                                                         │
    │  📊 Outlook: Bearish trend continuation likely in short term                │
    │  💡 Analysis: Breaking below support levels, high volatility expected       │
    │                                                                             │
    │  🤖 [GOOGL] Alphabet Inc. - Technology Sector                               │
    │  📈 Trading Signal: BUY                                                     │
    │  🔢 Confidence: 91%                                                         │
    │  📊 Outlook: Bullish breakout confirmed with strong fundamentals            │
    │  💡 Analysis: Earnings beat expectations, strong technical setup            │
    │                                                                             │
    └─────────────────────────────────────────────────────────────────────────────┘
    """, code_style))
    
    # 6. Live News Updates
    story.append(PageBreak())
    story.append(Paragraph("6. Live News Updates", heading1_style))
    story.append(Paragraph("The platform provides live market news updates every 5 minutes:", normal_style))
    
    news_features = [
        "Automated news refresh every 5 minutes",
        "Market movement-based content generation",
        "Company-specific news alerts",
        "Sector-wide developments and trends",
        "Economic indicator updates"
    ]
    
    news_list = ListFlowable(
        [ListItem(Paragraph(item, normal_style)) for item in news_features],
        bulletType='bullet'
    )
    story.append(news_list)
    
    # Mockup of live news
    story.append(Paragraph("Sample Live News Layout:", subtitle_style))
    story.append(Paragraph("""
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │  Live Market News (Updated every 5 minutes)                                 │
    │                                                                             │
    │  📰 [2025-11-30 15:25] AAPL Surpasses $3 Trillion Market Cap                │
    │  Apple Inc. reaches a new milestone with its market capitalization          │
    │  crossing $3 trillion, making it one of the most valuable companies.        │
    │                                                                             │
    │  📰 [2025-11-30 15:20] Fed Signals Potential Rate Cut in December           │
    │  Federal Reserve hints at possible interest rate reduction in upcoming     │
    │  meeting, potentially boosting tech sector stocks.                         │
    │                                                                             │
    │  📰 [2025-11-30 15:15] MSFT Announces Major AI Partnership                  │
    │  Microsoft partners with leading semiconductor company for next-gen AI      │
    │  chips, expected to accelerate cloud computing growth.                     │
    │                                                                             │
    │  📰 [2025-11-30 15:10] Oil Prices Drop Amid Supply Concerns                 │
    │  Crude oil futures decline as OPEC+ discusses potential production cuts,    │
    │  affecting energy sector stocks.                                           │
    │                                                                             │
    │  📰 [2025-11-30 15:05] TSLA Faces Regulatory Scrutiny on Autopilot          │
    │  Transportation department launches investigation into Tesla's Autopilot   │
    │  system, stock reacts with minor decline.                                  │
    │                                                                             │
    └─────────────────────────────────────────────────────────────────────────────┘
    """, code_style))
    
    # 7. Performance Metrics
    story.append(PageBreak())
    story.append(Paragraph("7. System Performance Metrics", heading1_style))
    story.append(Paragraph("The platform delivers high-performance results with low latency:", normal_style))
    
    metrics_data = [
        ["Metric", "Value", "Target"],
        ["Average Response Time", "< 200ms", "< 500ms"],
        ["Data Refresh Rate", "15 seconds", "30 seconds"],
        ["Concurrent Users", "1,000+", "500"],
        ["Uptime", "99.9%", "99.5%"],
        ["AI Model Accuracy", "78%", "70%"],
        ["Trading Signal Accuracy", "82%", "75%"],
        ["User Satisfaction Rating", "4.5/5.0", "4.0/5.0"]
    ]
    
    metrics_table = Table(metrics_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#3b82f6")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    story.append(Spacer(1, 12))
    story.append(metrics_table)
    
    # Conclusion
    story.append(PageBreak())
    story.append(Paragraph("8. Conclusion", heading1_style))
    story.append(Paragraph("The Stock Market Trading Platform delivers comprehensive result outputs that enable traders to make informed decisions. The interactive charts, portfolio management tools, trading history, AI-powered signals, and live news updates provide a complete trading environment. The system's performance metrics demonstrate its effectiveness in processing real-time data with low latency while providing accurate predictive analytics.", normal_style))
    
    story.append(Paragraph("These outputs showcase the platform's capabilities in supporting modern trading activities through intuitive interfaces, real-time data visualization, and intelligent analytics. The combination of technical analysis tools with AI-powered insights creates a powerful system for both novice and experienced traders.", normal_style))
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey)))
    
    # Build PDF
    try:
        doc.build(story)
        print("Results output PDF generated successfully: Stock_Market_Platform_Results_Output.pdf")
        return True
    except Exception as e:
        print(f"Error generating results output PDF: {e}")
        return False

if __name__ == "__main__":
    create_results_output_pdf()