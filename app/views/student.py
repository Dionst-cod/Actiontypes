from flask import Blueprint, render_template

student_views = Blueprint('student_views', __name__)

@student_views.route('/student')
def student_page():
    return render_template('student.html')
