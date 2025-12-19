from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/test-admin')
def test_admin():
    return "Admin blueprint working"
