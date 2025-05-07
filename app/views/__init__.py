from app.views.admin import admin_bp
from app.views.student import student_views

def register_views(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_views)
