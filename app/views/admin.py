from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.models import Student, Answer, Statement
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def dashboard():
    students = Student.query.all()
    student_data = []

    for student in students:
        answers = Answer.query.filter_by(student_number=student.student_number).count()
        completed = answers >= 20
        student_data.append({
            "name": student.name,
            "student_number": student.student_number,
            "student_class": student.student_class,
            "team": student.team,
            "completed": completed,
            "answers": answers
        })

    unique_classes = sorted(set(s["student_class"] for s in student_data if s["student_class"]))

    return render_template('admin/dashboard.html', students=student_data, unique_classes=unique_classes)


from flask import request, jsonify
from app import db

@admin_bp.route('/reset/<student_number>', methods=['POST'])
def reset_student_answers(student_number):
    Answer.query.filter_by(student_number=student_number).delete()
    db.session.commit()
    return jsonify({"message": "Antwoorden gereset."}), 200


@admin_bp.route('/student/<student_number>')
def student_detail(student_number):
    student = Student.query.filter_by(student_number=student_number).first()
    if not student:
        return "Student niet gevonden", 404

    answers = Answer.query.filter_by(student_number=student_number).all()
    completed = len(answers) >= 20
    statements = {s.statement_number: s for s in Statement.query.all()}

    return render_template(
    'admin/student_detail.html',
    student=student,
    answers=answers,
    statements=statements,
    completed=completed
  )


@admin_bp.route('/student/<student_number>', methods=['POST'])
def update_student(student_number):
    student = Student.query.filter_by(student_number=student_number).first()
    if not student:
        return "Student niet gevonden", 404

    student.student_class = request.form.get('student_class')
    student.team = request.form.get('team')
    db.session.commit()

    return redirect(url_for('admin.student_detail', student_number=student_number))


