import os
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def export_to_excel(expenses):
    output = BytesIO()
    
    # Convert list of dict-like sqlite3.Row to list of dicts
    data = []
    for exp in expenses:
        data.append({
            'Date': exp['date'],
            'Title': exp['title'],
            'Category': exp['category'],
            'Amount': exp['amount'],
            'Payment Type': exp['payment_type'],
            'Notes': exp['notes']
        })
        
    df = pd.DataFrame(data)
    
    # Write to BytesIO
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Expenses')
        
    output.seek(0)
    return output

def export_to_pdf(expenses, total_spent, current_month):
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    elements.append(Paragraph(f"Smart Expense Report - {current_month}", styles['Title']))
    elements.append(Spacer(1, 12))
    
    # Summary
    elements.append(Paragraph(f"Total Spent: {total_spent}", styles['Heading2']))
    elements.append(Spacer(1, 12))
    
    # Table Data
    data = [['Date', 'Title', 'Category', 'Amount', 'Type']]
    for exp in expenses:
        data.append([
            exp['date'],
            exp['title'],
            exp['category'],
            f"Rs. {exp['amount']}",
            exp['payment_type']
        ])
        
    # Create Table
    t = Table(data, colWidths=[80, 150, 100, 80, 80])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(t)
    doc.build(elements)
    
    output.seek(0)
    return output
