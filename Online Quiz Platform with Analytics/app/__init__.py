from flask import Flask
from app.config import Config
from app.models.db import mysql
from app.routes import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)

    from app.auth.routes import auth_bp
    from app.quiz.routes import quiz_bp
    from app.admin.routes import admin_bp
    from app.analytics.routes import analytics_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(main_bp)

    return app
