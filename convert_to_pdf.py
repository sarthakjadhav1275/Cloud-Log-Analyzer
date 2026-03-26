import markdown
import pdfkit
import os

def convert_markdown_to_pdf(md_file_path, pdf_file_path):
    """Convert Markdown file to PDF"""
    
    # Read the Markdown file
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()
    
    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    
    # Add CSS styling for better PDF appearance
    html_with_style = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Cloud Log Analyzer Project Report</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                margin: 40px;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1 {{
                color: #1f77b4;
                border-bottom: 3px solid #1f77b4;
                padding-bottom: 10px;
                page-break-after: avoid;
            }}
            h2 {{
                color: #003366;
                border-bottom: 2px solid #003366;
                padding-bottom: 5px;
                page-break-after: avoid;
            }}
            h3 {{
                color: #003366;
                page-break-after: avoid;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                page-break-inside: avoid;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            code {{
                background-color: #f4f4f4;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }}
            pre {{
                background-color: #f4f4f4;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                page-break-inside: avoid;
            }}
            blockquote {{
                border-left: 4px solid #1f77b4;
                margin-left: 0;
                padding-left: 20px;
                font-style: italic;
            }}
            ul, ol {{
                margin: 10px 0;
                padding-left: 30px;
            }}
            li {{
                margin: 5px 0;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .footer {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                text-align: center;
                font-size: 12px;
                color: #666;
            }}
            @page {{
                margin: 2cm;
                @bottom-center {{
                    content: counter(page);
                    font-size: 10px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Cloud Log Analyzer Project Report</h1>
            <p><strong>Course:</strong> Cloud Computing Lab (CCL) Mini-Project</p>
            <p><strong>Developer:</strong> Sarthak</p>
            <p><strong>Date:</strong> March 25, 2026</p>
        </div>
        
        {html_content}
        
        <div class="footer">
            <p>Generated from Cloud Log Analyzer Project Documentation</p>
        </div>
    </body>
    </html>
    """
    
    # Configure PDF options
    options = {
        'page-size': 'A4',
        'margin-top': '2cm',
        'margin-right': '2cm',
        'margin-bottom': '2cm',
        'margin-left': '2cm',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }
    
    try:
        # Convert HTML to PDF
        pdfkit.from_string(html_with_style, pdf_file_path, options=options)
        print(f"✅ Successfully converted {md_file_path} to {pdf_file_path}")
        return True
    except Exception as e:
        print(f"❌ Error converting to PDF: {e}")
        return False

if __name__ == "__main__":
    md_file = "Cloud_Log_Analyzer_Project_Report.md"
    pdf_file = "Cloud_Log_Analyzer_Project_Report.pdf"
    
    if os.path.exists(md_file):
        success = convert_markdown_to_pdf(md_file, pdf_file)
        if success:
            print(f"📄 PDF report created: {pdf_file}")
        else:
            print("❌ Failed to create PDF")
    else:
        print(f"❌ Markdown file not found: {md_file}")
