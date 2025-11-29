import markdown
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

def markdown_to_pdf(input_file, output_file):
    # Read the markdown file
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML
    html = markdown.markdown(markdown_content)
    
    # Create PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Split content by lines and process
    lines = html.split('\n')
    story = []
    
    # Title
    story.append(Paragraph("Stock Market Information System: Research Paper", title_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Process content
    for line in lines:
        if line.startswith('<h1>'):
            text = line.replace('<h1>', '').replace('</h1>', '')
            story.append(Paragraph(text, heading1_style))
        elif line.startswith('<h2>'):
            text = line.replace('<h2>', '').replace('</h2>', '')
            story.append(Paragraph(text, heading2_style))
        elif line.startswith('<h3>'):
            text = line.replace('<h3>', '').replace('</h3>', '')
            story.append(Paragraph(text, heading2_style))
        elif line.startswith('<p>') or '<p>' in line:
            text = line.replace('<p>', '').replace('</p>', '')
            story.append(Paragraph(text, normal_style))
        elif line.startswith('<li>'):
            text = line.replace('<li>', '• ').replace('</li>', '')
            story.append(Paragraph(text, normal_style))
        elif line.strip() == '':
            story.append(Spacer(1, 0.1*inch))
    
    # Build PDF
    doc.build(story)

if __name__ == "__main__":
    input_path = r"c:\Users\S PRAVEEN KUMAR\OneDrive\Desktop\Stock_market\Stock_Market_System_Research_Paper.md"
    output_path = r"c:\Users\S PRAVEEN KUMAR\OneDrive\Desktop\Stock_market\Stock_Market_System_Research_Paper.pdf"
    
    markdown_to_pdf(input_path, output_path)
    print(f"PDF created successfully at: {output_path}")