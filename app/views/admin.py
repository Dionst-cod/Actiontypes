from flask import Blueprint, render_template, redirect, url_for
from app.models import Student, Answer, Statement
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if 'teacher_id' not in session:
            flash("Log eerst in om toegang te krijgen.", "warning")
            return redirect(url_for('auth.login'))
        return view_func(*args, **kwargs)
    return wrapper


@admin_bp.route('/')
@login_required
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
    unique_teams = sorted(set(s["team"] for s in student_data if s["team"]))


    return render_template('admin/dashboard.html', students=student_data, unique_classes=unique_classes, unique_teams=unique_teams)


from flask import request, jsonify
from app import db

@admin_bp.route('/reset/<student_number>', methods=['POST'])
@login_required
def reset_student_answers(student_number):
    Answer.query.filter_by(student_number=student_number).delete()
    db.session.commit()
    return jsonify({"message": "Antwoorden gereset."}), 200


@admin_bp.route('/student/<student_number>')
@login_required
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
@login_required
def update_student(student_number):
    student = Student.query.filter_by(student_number=student_number).first()
    if not student:
        return "Student niet gevonden", 404

    student.student_class = request.form.get('student_class')
    student.team = request.form.get('team')
    db.session.commit()

    return redirect(url_for('admin.student_detail', student_number=student_number))

import csv
import io
from flask import Response

@admin_bp.route('/export')
def export_students():
    def generate():
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Studentnummer", "Naam", "Actiontype", "Datum", "Klas", "Team"])

        students = Student.query.all()
        for student in students:
            last_answer = (
                Answer.query
                .filter_by(student_number=student.student_number)
                .order_by(Answer.id.desc())
                .first()
            )
            date = last_answer.timestamp.strftime("%Y-%m-%d %H:%M:%S") if last_answer and last_answer.timestamp else "—"
            actiontype = student.actiontype if hasattr(student, 'actiontype') else "—"

            writer.writerow([
                student.student_number,
                student.name,
                actiontype,
                date,
                student.student_class,
                student.team or "—"
            ])

        output.seek(0)
        return output.getvalue()

    return Response(
        generate(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment; filename=studenten_export.csv"}
    )


