from flask import Blueprint, render_template, session, redirect, url_for, request
from app.models.db import mysql

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/quizzes')
def list_quizzes():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, title, description FROM quizzes")
    quizzes = cur.fetchall()
    cur.close()

    return render_template('quiz_list.html', quizzes=quizzes)

@quiz_bp.route('/quiz/start/<int:quiz_id>', methods=['GET', 'POST'])
def start_quiz(quiz_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        user_id = session['user_id']
        score = 0

        # Create attempt
        cur.execute(
            "INSERT INTO attempts (user_id, quiz_id, score) VALUES (%s,%s,%s)",
            (user_id, quiz_id, 0)
        )
        attempt_id = cur.lastrowid

        # Process answers
        for key, value in request.form.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                selected_option = int(value)

                cur.execute(
                    "SELECT is_correct FROM options WHERE id=%s",
                    (selected_option,)
                )
                is_correct = cur.fetchone()[0]

                if is_correct:
                    score += 1

                cur.execute(
                    "INSERT INTO responses (attempt_id, question_id, selected_option_id) VALUES (%s,%s,%s)",
                    (attempt_id, question_id, selected_option)
                )

        # Update score
        cur.execute(
            "UPDATE attempts SET score=%s WHERE id=%s",
            (score, attempt_id)
        )

        mysql.connection.commit()
        cur.close()

        return f"Quiz submitted. Your score: {score}"

    # GET request → show questions
    cur.execute("SELECT id, question FROM questions WHERE quiz_id=%s", (quiz_id,))
    questions = cur.fetchall()

    quiz_data = []
    for q in questions:
        cur.execute(
            "SELECT id, option_text FROM options WHERE question_id=%s",
            (q[0],)
        )
        options = cur.fetchall()
        quiz_data.append((q, options))

    cur.close()
    return render_template('take_quiz.html', quiz_data=quiz_data)
