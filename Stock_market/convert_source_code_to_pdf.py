import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime

def create_source_code_pdf():
    """
    Generate a PDF version of the source code for report inclusion
    """
    
    # Read the source code file
    source_code_path = "source_code_for_report.py"
    if not os.path.exists(source_code_path):
        print(f"Error: {source_code_path} not found")
        return False
    
    with open(source_code_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    # Create PDF document
    doc = SimpleDocTemplate("Stock_Market_Source_Code.pdf", pagesize=A4)
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
        fontSize=8,
        spaceAfter=6,
        fontName='Courier',
        backColor=colors.HexColor("#f8f9fa"),
        borderColor=colors.HexColor("#e9ecef"),
        borderWidth=1,
        borderPadding=8,
        borderRadius=3,
        leading=10
    )
    
    # Build content
    story = []
    
    # Title
    story.append(Paragraph("Stock Market Trading Platform", title_style))
    story.append(Paragraph("Source Code for Academic Report", styles['Heading2']))
    story.append(Paragraph("S. Praveen Kumar<br/>School of Computer Science<br/>Anna University<br/>Chennai, India", author_style))
    story.append(Spacer(1, 20))
    
    # Introduction
    story.append(Paragraph("1. Introduction", heading1_style))
    story.append(Paragraph(
        "This document contains the key source code components of the Stock Market Trading Platform "
        "that can be included in academic reports and publications. The platform is built using "
        "Python Flask framework with yfinance for real-time stock data, and provides features such as "
        "real-time stock charting with technical indicators, AI-powered trading signals, portfolio management, "
        "live news updates, and predictive analytics.", normal_style))
    
    # Split source code into sections for better presentation
    lines = source_code.split('\n')
    
    # Add source code to document
    story.append(Paragraph("2. Complete Source Code", heading1_style))
    
    # Process code in chunks to avoid memory issues
    current_chunk = []
    line_count = 0
    
    for line in lines:
        current_chunk.append(line)
        line_count += 1
        
        # Every 50 lines, add chunk to document
        if line_count % 50 == 0:
            chunk_text = '\n'.join(current_chunk)
            story.append(Paragraph(chunk_text.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>'), code_style))
            story.append(Spacer(1, 12))
            current_chunk = []
    
    # Add remaining lines
    if current_chunk:
        chunk_text = '\n'.join(current_chunk)
        story.append(Paragraph(chunk_text.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>'), code_style))
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey)))
    
    # Build PDF
    try:
        doc.build(story)
        print("Source code PDF generated successfully: Stock_Market_Source_Code.pdf")
        return True
    except Exception as e:
        print(f"Error generating source code PDF: {e}")
        return False

if __name__ == "__main__":
    create_source_code_pdf()