from flask import Blueprint, render_template, redirect, url_for
from app.models import Student, Answer, Statement
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


from functools import wraps
from flask import session, redirect, url_for, flash

def calculate_action_type(student_number):
    answers = Answer.query.filter_by(student_number=student_number).all()
    if len(answers) == 0:
        return None

    statements = {s.statement_number: s for s in Statement.query.all()}

    trait_scores = {
        'EI': {'E': 0, 'I': 0},
        'SN': {'S': 0, 'N': 0},
        'TF': {'T': 0, 'F': 0},
        'JP': {'J': 0, 'P': 0},
    }

    trait_map = {
        'EI': ['E', 'I'],
        'SN': ['S', 'N'],
        'TF': ['T', 'F'],
        'JP': ['J', 'P'],
    }

    for answer in answers:
        stmt = statements.get(answer.statement_number)
        if not stmt:
            continue

        pair = stmt.trait_type
        if pair not in trait_map:
            continue

        
        trait_index = answer.choice_number - 1  
        selected_trait = trait_map[pair][trait_index]

        trait_scores[pair][selected_trait] += 1

    action_type = ''
    for pair in ['EI', 'SN', 'TF', 'JP']:
        score = trait_scores[pair]
        if score[trait_map[pair][0]] >= score[trait_map[pair][1]]:
            action_type += trait_map[pair][0]
        else:
            action_type += trait_map[pair][1]

    return action_type


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if 'teacher_id' not in session:
            flash("Log eerst in om toegang te krijgen.", "warning")
            return redirect(url_for('auth.login'))
        return view_func(*args, **kwargs)
    return wrapper


@admin_bp.route('/logout')
def logout():
    session.clear()
    flash("Je bent uitgelogd.", "info")
    return redirect(url_for('auth.login'))


@admin_bp.route('/')
@login_required
def dashboard():
    students = Student.query.all()
    student_data = []

    for student in students:
        answers = Answer.query.filter_by(student_number=student.student_number).count()
        completed = answers >= 20
        action_type = calculate_action_type(student.student_number)
        student_data.append({
            "name": student.name,
            "student_number": student.student_number,
            "student_class": student.student_class,
            "team": student.team,
            "completed": completed,
            "answers": answers,
            "action_type": action_type  
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

    action_type = calculate_action_type(student.student_number)

    return render_template(
        'admin/student_detail.html',
        student=student,
        answers=answers,
        statements=statements,
        completed=completed,
        action_type=action_type 
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
            actiontype = calculate_action_type(student.student_number) or "—"

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


@admin_bp.route('/teachers')
@login_required
def manage_teachers():
    if not session.get('is_admin'):
        flash("Alleen admins mogen docenten beheren.", "danger")
        return redirect(url_for('admin.dashboard'))

    teachers = Teacher.query.all()
    return render_template('admin/teachers.html', teachers=teachers)

from app.models import Teacher
from werkzeug.security import generate_password_hash


@admin_bp.route('/teachers', methods=['POST'])
@login_required
def add_teacher():
    if not session.get('is_admin'):
        flash("Alleen admins mogen docenten toevoegen.", "danger")
        return redirect(url_for('admin.dashboard'))

    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = bool(request.form.get('is_admin'))

    if not (name and username and password):
        flash("Vul alle verplichte velden in.", "warning")
        return redirect(url_for('admin.manage_teachers'))

    existing = Teacher.query.filter_by(username=username).first()
    if existing:
        flash("Gebruikersnaam bestaat al.", "danger")
        return redirect(url_for('admin.manage_teachers'))

    new_teacher = Teacher(
        name=name,
        username=username,
        is_admin=is_admin
    )
    new_teacher.set_password(password)
    db.session.add(new_teacher)
    db.session.commit()

    flash("Docent toegevoegd!", "success")
    return redirect(url_for('admin.manage_teachers'))


@admin_bp.route('/student', methods=['POST'])
@login_required
def add_student():
    student_number = request.form.get('student_number')
    name = request.form.get('name')
    student_class = request.form.get('student_class')

    if not all([student_number, name, student_class]):
        flash("Vul alle velden in.", "warning")
        return redirect(url_for('admin.dashboard'))

    if Student.query.filter_by(student_number=student_number).first():
        flash("Studentnummer bestaat al.", "danger")
        return redirect(url_for('admin.dashboard'))

    new_student = Student(
        student_number=student_number,
        name=name,
        student_class=student_class
    )

    db.session.add(new_student)
    db.session.commit()

    flash("Student toegevoegd!", "success")
    return redirect(url_for('admin.dashboard'))
