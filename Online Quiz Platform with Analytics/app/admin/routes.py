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

@admin_bp.route('/add-question/<int:quiz_id>', methods=['GET', 'POST'])
def add_question(quiz_id):
    admin_required()

    if request.method == 'POST':
        question_text = request.form['question']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO questions (quiz_id, question) VALUES (%s, %s)",
            (quiz_id, question_text)
        )
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('admin.add_question', quiz_id=quiz_id))

    return render_template('add_question.html', quiz_id=quiz_id)

@admin_bp.route('/add-option/<int:question_id>', methods=['GET', 'POST'])
def add_option(question_id):
    admin_required()

    if request.method == 'POST':
        option_text = request.form['option']
        is_correct = request.form.get('is_correct') == 'on'

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO options (question_id, option_text, is_correct) VALUES (%s,%s,%s)",
            (question_id, option_text, is_correct)
        )
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('admin.add_option', question_id=question_id))

    return render_template('add_option.html', question_id=question_id)

@admin_bp.route('/analytics')
def quiz_analytics():
    admin_required()

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT q.title, COUNT(a.id) AS attempts, AVG(a.score) AS avg_score
        FROM quizzes q
        LEFT JOIN attempts a ON q.id = a.quiz_id
        GROUP BY q.id
    """)
    data = cur.fetchall()
    cur.close()

    return render_template('admin_analytics.html', data=data)
