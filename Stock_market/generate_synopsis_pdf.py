import markdown
import pdfkit
import os
from datetime import datetime

def generate_synopsis_pdf():
    """
    Generate a PDF version of the project synopsis that can be uploaded anywhere
    """
    
    # Read the markdown synopsis
    synopsis_path = "project_synopsis.md"
    if not os.path.exists(synopsis_path):
        print(f"Error: {synopsis_path} not found")
        return False
    
    with open(synopsis_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])
    
    # Add CSS styling for better presentation
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Stock Market Trading Platform - Project Synopsis</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1, h2, h3, h4 {{
                color: #2c3e50;
            }}
            h1 {{
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                border-bottom: 2px solid #3498db;
                padding-bottom: 5px;
                margin-top: 30px;
            }}
            h3 {{
                color: #3498db;
                margin-top: 25px;
            }}
            code {{
                background-color: #f8f9fa;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: monospace;
            }}
            pre {{
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }}
            ul, ol {{
                padding-left: 20px;
            }}
            li {{
                margin-bottom: 5px;
            }}
            .diagram {{
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                font-family: monospace;
                text-align: center;
            }}
            footer {{
                margin-top: 50px;
                text-align: center;
                font-size: 0.9em;
                color: #7f8c8d;
                border-top: 1px solid #ecf0f1;
                padding-top: 20px;
            }}
        </style>
    </head>
    <body>
        {html_content}
        <footer>
            Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}<br>
            Stock Market Trading Platform - Project Synopsis
        </footer>
    </body>
    </html>
    """
    
    # Generate PDF
    try:
        # Configure pdfkit to use wkhtmltopdf
        # Note: wkhtmltopdf must be installed on the system
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_string(styled_html, 'project_synopsis.pdf', configuration=config)
        print("PDF generated successfully: project_synopsis.pdf")
        return True
    except OSError as e:
        # If wkhtmltopdf is not installed, try without configuration
        try:
            pdfkit.from_string(styled_html, 'project_synopsis.pdf')
            print("PDF generated successfully: project_synopsis.pdf")
            return True
        except Exception as e2:
            print(f"Error generating PDF: {e2}")
            # Save HTML as backup
            with open('project_synopsis.html', 'w', encoding='utf-8') as f:
                f.write(styled_html)
            print("Saved HTML version as backup: project_synopsis.html")
            return False
    except Exception as e:
        print(f"Error generating PDF: {e}")
        # Save HTML as backup
        with open('project_synopsis.html', 'w', encoding='utf-8') as f:
            f.write(styled_html)
        print("Saved HTML version as backup: project_synopsis.html")
        return False

if __name__ == "__main__":
    generate_synopsis_pdf()