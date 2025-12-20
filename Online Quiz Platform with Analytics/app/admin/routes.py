from flask import Blueprint, render_template, redirect, url_for, session, abort, request
from app.models.db import mysql

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required():
    if session.get('role') != 'admin':
        abort(403)

@admin_bp.route('/dashboard')
def dashboard():
    admin_required()
    return "Admin Dashboard"

@admin_bp.route('/create-quiz', methods=['GET', 'POST'])
def create_quiz():
    admin_required()

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        time_limit = request.form['time_limit']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO quizzes (title, description, time_limit) VALUES (%s,%s,%s)",
            (title, desc, time_limit)
        )
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('admin.dashboard'))

    return render_template('create_quiz.html')
