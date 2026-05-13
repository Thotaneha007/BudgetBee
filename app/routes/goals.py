from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app.routes.auth import login_required

goals_bp = Blueprint('goals', __name__)

@goals_bp.route('/goals', methods=['GET', 'POST'])
@login_required
def goals_view():
    db = current_app.get_db()
    cursor = db.cursor()
    user_id = session['user_id']
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            name = request.form.get('name', '').strip()
            target_str = request.form.get('target_amount', '0')
            deadline = request.form.get('deadline')
            
            if not name or not target_str:
                flash('Goal name and target amount are required', 'error')
                return redirect(url_for('goals.goals_view'))
                
            try:
                target_amount = float(target_str)
                if target_amount <= 0:
                    flash('Target amount must be positive', 'error')
                    return redirect(url_for('goals.goals_view'))
            except ValueError:
                flash('Invalid amount format', 'error')
                return redirect(url_for('goals.goals_view'))
                
            cursor.execute('''
                INSERT INTO goals (user_id, name, target_amount, current_amount, deadline)
                VALUES (?, ?, ?, 0, ?)
            ''', (user_id, name, target_amount, deadline))
            db.commit()
            flash('Goal created successfully!', 'success')
            
        elif action == 'update':
            goal_id = request.form.get('goal_id')
            amount_str = request.form.get('amount', '0')
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    flash('Savings amount must be positive', 'error')
                    return redirect(url_for('goals.goals_view'))
            except ValueError:
                flash('Invalid amount format', 'error')
                return redirect(url_for('goals.goals_view'))
            
            cursor.execute('''
                UPDATE goals 
                SET current_amount = current_amount + ? 
                WHERE id = ? AND user_id = ?
            ''', (amount, goal_id, user_id))
            db.commit()
            flash('Progress updated!', 'success')
            
        return redirect(url_for('goals.goals_view'))
        
    # GET: fetch goals
    cursor.execute('SELECT * FROM goals WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    goals_list = cursor.fetchall()
    
    return render_template('goals.html', goals=goals_list)

@goals_bp.route('/goal/delete/<int:id>', methods=['POST'])
@login_required
def delete_goal(id):
    db = current_app.get_db()
    cursor = db.cursor()
    user_id = session['user_id']
    
    cursor.execute('DELETE FROM goals WHERE id = ? AND user_id = ?', (id, user_id))
    db.commit()
    flash('Goal deleted.', 'success')
    return redirect(url_for('goals.goals_view'))
