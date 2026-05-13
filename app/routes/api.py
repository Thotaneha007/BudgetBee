import os
from datetime import date
from flask import Blueprint, jsonify, session, current_app, request, send_file
from app.routes.auth import login_required
from app.utils.ai import generate_financial_insights
from app.utils.export import export_to_pdf, export_to_excel
from app.utils.ocr import extract_receipt_data

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/chart-data')
@login_required
def chart_data():
    db = current_app.get_db()
    cursor = db.cursor()
    user_id = session['user_id']
    current_month = date.today().strftime('%Y-%m')
    
    # Data for Category Pie Chart (Current Month)
    cursor.execute('''
        SELECT category, SUM(amount) as total 
        FROM expenses 
        WHERE user_id = ? AND strftime('%Y-%m', date) = ?
        GROUP BY category
    ''', (user_id, current_month))
    category_data = {row['category']: row['total'] for row in cursor.fetchall()}
    
    # Data for Monthly Trend (Last 6 Months) - Expenses vs Income
    cursor.execute('''
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM expenses
        WHERE user_id = ?
        GROUP BY month
        ORDER BY month DESC
        LIMIT 6
    ''', (user_id,))
    expense_trend = {row['month']: row['total'] for row in cursor.fetchall()}
    
    cursor.execute('''
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM income
        WHERE user_id = ?
        GROUP BY month
        ORDER BY month DESC
        LIMIT 6
    ''', (user_id,))
    income_trend = {row['month']: row['total'] for row in cursor.fetchall()}
    
    # Merge months and ensure they are sorted
    all_months = sorted(list(set(list(expense_trend.keys()) + list(income_trend.keys()))))
    trend_data = {
        'months': all_months,
        'expenses': [expense_trend.get(m, 0) for m in all_months],
        'income': [income_trend.get(m, 0) for m in all_months]
    }
    
    # Data for Yearly Trend (Last 12 Months)
    cursor.execute('''
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM expenses
        WHERE user_id = ?
        GROUP BY month
        ORDER BY month DESC
        LIMIT 12
    ''', (user_id,))
    ye_rows = {row['month']: row['total'] for row in cursor.fetchall()}
    
    cursor.execute('''
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM income
        WHERE user_id = ?
        GROUP BY month
        ORDER BY month DESC
        LIMIT 12
    ''', (user_id,))
    yi_rows = {row['month']: row['total'] for row in cursor.fetchall()}
    
    ym_labels = sorted(list(set(list(ye_rows.keys()) + list(yi_rows.keys()))))
    yearly_data = {
        'months': ym_labels,
        'expenses': [ye_rows.get(m, 0) for m in ym_labels],
        'income': [yi_rows.get(m, 0) for m in ym_labels]
    }
    
    # Data for True Yearly Trend (All Years)
    cursor.execute('''
        SELECT strftime('%Y', date) as year, SUM(amount) as total
        FROM expenses
        WHERE user_id = ?
        GROUP BY year
        ORDER BY year ASC
    ''', (user_id,))
    yearly_expense_rows = cursor.fetchall()
    
    cursor.execute('''
        SELECT strftime('%Y', date) as year, SUM(amount) as total
        FROM income
        WHERE user_id = ?
        GROUP BY year
        ORDER BY year ASC
    ''', (user_id,))
    yearly_income_rows = cursor.fetchall()
    
    # Yearly Income vs Expense
    yearly_years = sorted(list(set([row['year'] for row in yearly_expense_rows] + [row['year'] for row in yearly_income_rows])))
    exp_map = {row['year']: row['total'] for row in yearly_expense_rows}
    inc_map = {row['year']: row['total'] for row in yearly_income_rows}
    
    yearly_stats = {
        'years': yearly_years,
        'expenses': [exp_map.get(y, 0) for y in yearly_years],
        'income': [inc_map.get(y, 0) for y in yearly_years],
        'savings': [inc_map.get(y, 0) - exp_map.get(y, 0) for y in yearly_years]
    }
    
    # Highest Spending Month (Current Year)
    cursor.execute('''
        SELECT strftime('%m', date) as month, SUM(amount) as total
        FROM expenses
        WHERE user_id = ? AND strftime('%Y', date) = strftime('%Y', 'now')
        GROUP BY month
        ORDER BY total DESC
        LIMIT 1
    ''', (user_id,))
    peak_month = cursor.fetchone()
    
    return jsonify({
        'categories': category_data,
        'trend': trend_data,
        'yearly': yearly_data, # Keeping 12-month trend as well
        'true_yearly': yearly_stats,
        'peak_month': peak_month['month'] if peak_month else None,
        'peak_amount': peak_month['total'] if peak_month else 0
    })

@api_bp.route('/api/insights')
@login_required
def get_insights():
    db = current_app.get_db()
    cursor = db.cursor()
    user_id = session['user_id']
    current_month = date.today().strftime('%Y-%m')
    
    # Get budget
    cursor.execute("SELECT amount FROM budgets WHERE user_id = ? AND month = ?", (user_id, current_month))
    budget_row = cursor.fetchone()
    budget_amt = budget_row['amount'] if budget_row else 0.0
    
    # Get total spent
    cursor.execute("SELECT SUM(amount) as total FROM expenses WHERE user_id = ? AND strftime('%Y-%m', date) = ?", (user_id, current_month))
    spent = cursor.fetchone()['total'] or 0.0
    
    # Get total income
    cursor.execute("SELECT SUM(amount) as total FROM income WHERE user_id = ? AND strftime('%Y-%m', date) = ?", (user_id, current_month))
    income = cursor.fetchone()['total'] or 0.0
    
    # Get expenses
    cursor.execute("SELECT title, amount, category FROM expenses WHERE user_id = ? AND strftime('%Y-%m', date) = ?", (user_id, current_month))
    expenses = [dict(row) for row in cursor.fetchall()]
    
    insights = generate_financial_insights(expenses, budget_amt, spent, income, current_month)
    return jsonify({'insights': insights})

@api_bp.route('/settings/language', methods=['POST'])
@login_required
def set_language():
    lang = request.json.get('language')
    if lang in ['en', 'hi', 'te']:
        session['language'] = lang
        db = current_app.get_db()
        cursor = db.cursor()
        cursor.execute('UPDATE users SET language = ? WHERE id = ?', (lang, session['user_id']))
        db.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Invalid language'}), 400

@api_bp.route('/export/pdf')
@login_required
def export_pdf():
    db = current_app.get_db()
    cursor = db.cursor()
    user_id = session['user_id']
    current_month = date.today().strftime('%Y-%m')
    
    cursor.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC', (user_id,))
    expenses = cursor.fetchall()
    
    cursor.execute('SELECT SUM(amount) as total FROM expenses WHERE user_id = ?', (user_id,))
    total_spent = cursor.fetchone()['total'] or 0.0
    
    pdf_stream = export_to_pdf(expenses, total_spent, current_month)
    return send_file(pdf_stream, as_attachment=True, download_name=f"Expenses_{current_month}.pdf", mimetype='application/pdf')

@api_bp.route('/export/excel')
@login_required
def export_excel():
    db = current_app.get_db()
    cursor = db.cursor()
    user_id = session['user_id']
    
    cursor.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC', (user_id,))
    expenses = cursor.fetchall()
    
    excel_stream = export_to_excel(expenses)
    return send_file(excel_stream, as_attachment=True, download_name="All_Expenses.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@api_bp.route('/api/ocr', methods=['POST'])
@login_required
def ocr_receipt():
    if 'receipt' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
        
    file = request.files['receipt']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    data = extract_receipt_data(file.stream)
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'Failed to extract data'}), 500
