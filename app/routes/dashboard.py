from flask import Blueprint, render_template, session, current_app
from datetime import date
from app.routes.auth import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard_view():
    db = current_app.get_db()
    cursor = db.cursor()
    user_id = session['user_id']
    
    current_month = date.today().strftime('%Y-%m')
    
    # Total Expenses
    cursor.execute('SELECT SUM(amount) as total FROM expenses WHERE user_id = ?', (user_id,))
    total_spent = cursor.fetchone()['total'] or 0.0
    
    # Monthly Expenses
    cursor.execute("SELECT SUM(amount) as total FROM expenses WHERE user_id = ? AND strftime('%Y-%m', date) = ?", (user_id, current_month))
    monthly_spent = cursor.fetchone()['total'] or 0.0
    
    # Total Income
    cursor.execute('SELECT SUM(amount) as total FROM income WHERE user_id = ?', (user_id,))
    total_income = cursor.fetchone()['total'] or 0.0
    
    # Monthly Income
    cursor.execute("SELECT SUM(amount) as total FROM income WHERE user_id = ? AND strftime('%Y-%m', date) = ?", (user_id, current_month))
    monthly_income = cursor.fetchone()['total'] or 0.0
    
    # Budget
    cursor.execute("SELECT amount FROM budgets WHERE user_id = ? AND month = ?", (user_id, current_month))
    budget_row = cursor.fetchone()
    monthly_budget = budget_row['amount'] if budget_row else 0.0
    
    # Subscription & Recurring Totals
    cursor.execute("SELECT SUM(amount) as total FROM expenses WHERE user_id = ? AND is_subscription = 1 AND strftime('%Y-%m', date) = ?", (user_id, current_month))
    monthly_subs = cursor.fetchone()['total'] or 0.0
    
    cursor.execute("SELECT SUM(amount) as total FROM expenses WHERE user_id = ? AND is_recurring = 1 AND strftime('%Y-%m', date) = ?", (user_id, current_month))
    monthly_recurring = cursor.fetchone()['total'] or 0.0
    
    # Recent Expenses
    cursor.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT 5', (user_id,))
    recent_expenses = cursor.fetchall()
    
    # Financial Calculations
    monthly_savings = monthly_income - monthly_spent
    total_balance = total_income - total_spent
    
    # Financial Health Score (0-100)
    health_score = 0
    if monthly_income > 0:
        savings_rate = (monthly_savings / monthly_income)
        health_score = min(max(int(savings_rate * 100), 0), 100)
    
    return render_template('dashboard.html', 
                           total_spent=total_spent, 
                           monthly_spent=monthly_spent,
                           monthly_budget=monthly_budget,
                           total_income=total_income,
                           monthly_income=monthly_income,
                           monthly_savings=monthly_savings,
                           total_balance=total_balance,
                           monthly_subs=monthly_subs,
                           monthly_recurring=monthly_recurring,
                           health_score=health_score,
                           recent_expenses=recent_expenses,
                           current_month=current_month)

@dashboard_bp.route('/budget', methods=['GET', 'POST'])
@login_required
def budget():
    from flask import request, flash, redirect, url_for
    db = current_app.get_db()
    cursor = db.cursor()
    user_id = session['user_id']
    current_month = date.today().strftime('%Y-%m')
    
    if request.method == 'POST':
        month = request.form.get('month')
        amount_str = request.form.get('amount', '0')
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                flash('Budget amount must be positive', 'error')
                return redirect(url_for('dashboard.budget'))
        except ValueError:
            flash('Invalid amount format', 'error')
            return redirect(url_for('dashboard.budget'))
            
        cursor.execute('SELECT id FROM budgets WHERE user_id = ? AND month = ?', (user_id, month))
        if cursor.fetchone():
            cursor.execute('UPDATE budgets SET amount = ? WHERE user_id = ? AND month = ?', (amount, user_id, month))
        else:
            cursor.execute('INSERT INTO budgets (user_id, amount, month) VALUES (?, ?, ?)', (user_id, amount, month))
        db.commit()
        flash('Budget updated successfully', 'success')
        return redirect(url_for('dashboard.budget'))
        
    # GET: Fetch budgets with filter
    filter_year = request.args.get('year', '')
    query = 'SELECT * FROM budgets WHERE user_id = ?'
    params = [user_id]
    
    if filter_year:
        query += " AND substr(month, 1, 4) = ?"
        params.append(filter_year)
        
    query += ' ORDER BY month DESC'
    cursor.execute(query, params)
    budgets = cursor.fetchall()
    
    return render_template('budget.html', budgets=budgets, current_month=current_month)

@dashboard_bp.route('/settings')
@login_required
def settings():
    return render_template('settings.html')
