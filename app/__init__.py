from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    from app.models import Student, Statement, Answer, Teacher

    from app.api.api import bp as api_bp
    from app.views.auth import auth_bp
    from app.views import register_views

    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    register_views(app)

    return app
