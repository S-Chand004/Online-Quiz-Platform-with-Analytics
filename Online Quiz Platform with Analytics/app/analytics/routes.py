from flask import Blueprint

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/test-analytics')
def test_auth():
    return "Analytics blueprint working"
