from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from app.models import Teacher

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        teacher = Teacher.query.filter_by(username=username).first()

        if teacher and check_password_hash(teacher.password_hash, password):
            session['teacher_id'] = teacher.id
            session['is_admin'] = teacher.is_admin
            return redirect(url_for('admin.dashboard'))
        else:
            flash("Ongeldige inloggegevens", "danger")

    return render_template('admin/login.html')
