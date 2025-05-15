from flask import Blueprint, jsonify, request
from app.models import Student, Statement, Answer
from app import db
from sqlalchemy import not_
from datetime import datetime  

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/student/<student_number>/statement', methods=['GET'])
def get_next_statement(student_number):
    student = Student.query.filter_by(student_number=student_number).first()
    if not student:
        return {"error": "Student not found."}, 404
    
    total_statements = Statement.query.count()
    answered_count = Answer.query.filter_by(student_number=student_number).count()

    if answered_count >= total_statements:
        return {"error": "Test al voltooid"}, 403

    answered = db.session.query(Answer.statement_number).filter_by(student_number=student_number).subquery()

    statement = Statement.query.filter(Statement.statement_number.not_in(answered)).order_by(Statement.statement_number).first()

    if not statement:
        return {}

    response = {
    "statement_number": statement.statement_number,
    "statement_choices": [
        {"choice_number": 1, "choice_text": statement.choice_1_text},
        {"choice_number": 2, "choice_text": statement.choice_2_text}
    ],
    "name": student.name,
    "class": student.student_class  
    }
    return jsonify(response)


@bp.route('/student/<student_number>/statement/<int:statement_number>', methods=['POST'])
def submit_answer(student_number, statement_number):
    student = Student.query.filter_by(student_number=student_number).first()
    if not student:
        return {"error": "Student not found."}, 404

    data = request.get_json()
    choice_number = data.get('statement_choice')

    if not choice_number:
        return {"error": "Missing statement_choice"}, 400

    if not statement_number or not choice_number:
        return {"error": "Missing statement_number or choice_number"}, 400

    existing_answer = Answer.query.filter_by(
        student_number=student_number,
        statement_number=statement_number
    ).first()

    if existing_answer:
        return {"message": "Statement already answered."}, 409

    answer = Answer(
        student_number=student_number,
        statement_number=statement_number,
        choice_number=choice_number,
        timestamp=datetime.utcnow()
    )
    db.session.add(answer)
    db.session.commit()

    return {"result": "ok"}, 201


