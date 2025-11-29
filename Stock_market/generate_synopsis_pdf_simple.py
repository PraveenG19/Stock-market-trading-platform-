import markdown
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def markdown_to_plain_text(md_text):
    """Convert markdown to plain text for PDF generation"""
    # Simple conversion - remove markdown formatting
    import re
    
    # Remove headers
    text = re.sub(r'^#+\s*', '', md_text, flags=re.MULTILINE)
    
    # Remove bold/italic
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    
    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    
    # Remove links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # Remove images
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', text)
    
    # Convert lists
    text = re.sub(r'^\s*-\s*', '• ', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\*\s*', '• ', text, flags=re.MULTILINE)
    
    return text

def generate_synopsis_pdf():
    """
    Generate a PDF version of the project synopsis using ReportLab
    """
    
    # Read the markdown synopsis
    synopsis_path = "project_synopsis.md"
    if not os.path.exists(synopsis_path):
        print(f"Error: {synopsis_path} not found")
        return False
    
    with open(synopsis_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to plain text
    plain_text = markdown_to_plain_text(markdown_content)
    
    # Split into lines
    lines = plain_text.split('\n')
    
    # Create PDF document
    doc = SimpleDocTemplate("project_synopsis.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12,
        spaceBefore=20
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=15
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Build content
    story = []
    
    # Title
    story.append(Paragraph("Stock Market Trading Platform", title_style))
    story.append(Paragraph("Project Synopsis", styles['Heading2']))
    story.append(Spacer(1, 20))
    
    # Process lines
    for line in lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 6))
        elif line.startswith('# ') or line.startswith('## ') or line.startswith('### ') or line.startswith('#### '):
            # Headers
            level = line.count('#')
            content = line.lstrip('# ')
            if level == 1:
                story.append(Paragraph(content, heading1_style))
            elif level == 2:
                story.append(Paragraph(content, heading2_style))
            else:
                story.append(Paragraph(content, styles['Heading3']))
        elif line.startswith('• ') or line.startswith('- ') or line.startswith('* '):
            # List items
            content = line[2:]  # Remove bullet
            story.append(Paragraph(f"• {content}", normal_style))
        elif line.startswith('---'):
            # Horizontal rule
            story.append(Spacer(1, 12))
        else:
            # Regular paragraph
            story.append(Paragraph(line, normal_style))
    
    # Add footer
    story.append(Spacer(1, 30))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey)))
    story.append(Paragraph("Stock Market Trading Platform - Project Synopsis", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey)))
    
    # Build PDF
    try:
        doc.build(story)
        print("PDF generated successfully: project_synopsis.pdf")
        return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False

if __name__ == "__main__":
    generate_synopsis_pdf()