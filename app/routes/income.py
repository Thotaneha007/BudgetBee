from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app.routes.auth import login_required

income_bp = Blueprint('income', __name__)

@income_bp.route('/income', methods=['GET', 'POST'])
@login_required
def income_view():
    db = current_app.get_db()
    cursor = db.cursor()
    user_id = session['user_id']
    
    if request.method == 'POST':
        source = request.form.get('source', '').strip()
        amount_str = request.form.get('amount', '0')
        category = request.form.get('category')
        income_date = request.form.get('date')
        
        if not source or not amount_str or not income_date:
            flash('Source, Amount, and Date are required', 'error')
            return redirect(url_for('income.income_view'))
            
        try:
            amount = float(amount_str)
            if amount <= 0:
                flash('Amount must be positive', 'error')
                return redirect(url_for('income.income_view'))
        except ValueError:
            flash('Invalid amount format', 'error')
            return redirect(url_for('income.income_view'))
            
        notes = request.form.get('notes', '')
        
        cursor.execute('''
            INSERT INTO income (user_id, source, amount, category, date, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, source, amount, category, income_date, notes))
        db.commit()
        flash('Income added successfully', 'success')
        return redirect(url_for('income.income_view'))
        
    # GET: fetch income, optionally filter
    filter_month = request.args.get('month', '')
    filter_category = request.args.get('category', '')
    filter_min = request.args.get('min_amount', '')
    
    query = 'SELECT * FROM income WHERE user_id = ?'
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
    income_list = cursor.fetchall()
    
    return render_template('income.html', income=income_list)

@income_bp.route('/income/delete/<int:id>', methods=['POST'])
@login_required
def delete_income(id):
    db = current_app.get_db()
    cursor = db.cursor()
    user_id = session['user_id']
    
    cursor.execute('DELETE FROM income WHERE id = ? AND user_id = ?', (id, user_id))
    db.commit()
    flash('Income deleted successfully', 'success')
    return redirect(request.referrer or url_for('income.income_view'))
