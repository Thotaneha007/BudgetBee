from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app.routes.auth import login_required

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses_view():
    db = current_app.get_db()
    cursor = db.cursor()
    user_id = session['user_id']
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        amount_str = request.form.get('amount', '0')
        category = request.form.get('category')
        expense_date = request.form.get('date')
        payment_type = request.form.get('payment_type')
        
        if not title or not amount_str or not category or not expense_date:
            flash('All required fields must be filled', 'error')
            return redirect(url_for('expenses.expenses_view'))
            
        try:
            amount = float(amount_str)
            if amount <= 0:
                flash('Amount must be positive', 'error')
                return redirect(url_for('expenses.expenses_view'))
        except ValueError:
            flash('Invalid amount format', 'error')
            return redirect(url_for('expenses.expenses_view'))
            
        notes = request.form.get('notes', '')
        is_recurring = 1 if 'is_recurring' in request.form else 0
        recurring_freq = request.form.get('recurring_freq') if is_recurring else None
        is_subscription = 1 if 'is_subscription' in request.form else 0
        
        cursor.execute('''
            INSERT INTO expenses (user_id, title, amount, category, date, notes, payment_type, is_recurring, recurring_freq, is_subscription)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, title, amount, category, expense_date, notes, payment_type, is_recurring, recurring_freq, is_subscription))
        db.commit()
        flash('Expense added successfully', 'success')
        return redirect(url_for('expenses.expenses_view'))
        
    # GET: fetch expenses, optionally filter
    filter_month = request.args.get('month', '')
    filter_category = request.args.get('category', '')
    filter_min = request.args.get('min_amount', '')
    
    query = 'SELECT * FROM expenses WHERE user_id = ?'
    params = [user_id]
    
    if filter_month:
        query += " AND strftime('%Y-%m', date) = ?"
        params.append(filter_month)
    if filter_category:
        query += " AND category = ?"
        params.append(filter_category)
    if filter_min:
        query += " AND amount >= ?"
        params.append(float(filter_min))
        
    query += ' ORDER BY date DESC, id DESC'
    
    cursor.execute(query, params)
    expenses_list = cursor.fetchall()
    
    return render_template('expenses.html', expenses=expenses_list)

@expenses_bp.route('/expense/delete/<int:id>', methods=['POST'])
@login_required
def delete_expense(id):
    db = current_app.get_db()
    cursor = db.cursor()
    user_id = session['user_id']
    
    cursor.execute('DELETE FROM expenses WHERE id = ? AND user_id = ?', (id, user_id))
    db.commit()
    flash('Expense deleted successfully', 'success')
    return redirect(request.referrer or url_for('expenses.expenses_view'))

@expenses_bp.route('/export/excel')
@login_required
def export_excel():
    from flask import send_file
    from app.utils.export import export_to_excel
    
    db = current_app.get_db()
    cursor = db.cursor()
    user_id = session['user_id']
    
    cursor.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC', (user_id,))
    expenses = cursor.fetchall()
    
    output = export_to_excel(expenses)
    return send_file(output, as_attachment=True, download_name='BudgetBee_Expenses.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@expenses_bp.route('/export/pdf')
@login_required
def export_pdf():
    from flask import send_file
    from app.utils.export import export_to_pdf
    from datetime import date
    
    db = current_app.get_db()
    cursor = db.cursor()
    user_id = session['user_id']
    current_month = date.today().strftime('%Y-%m')
    
    cursor.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC', (user_id,))
    expenses = cursor.fetchall()
    
    cursor.execute("SELECT SUM(amount) as total FROM expenses WHERE user_id = ? AND strftime('%Y-%m', date) = ?", (user_id, current_month))
    total_spent = cursor.fetchone()['total'] or 0.0
    
    output = export_to_pdf(expenses, total_spent, current_month)
    return send_file(output, as_attachment=True, download_name=f'BudgetBee_Report_{current_month}.pdf', mimetype='application/pdf')
