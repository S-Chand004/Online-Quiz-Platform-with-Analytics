from flask import Blueprint

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/test-quiz')
def test_quiz():
    return "Quiz blueprint working"
