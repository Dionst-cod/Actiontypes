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

    answered = db.session.query(Answer.statement_number).filter_by(student_number=student_number).subquery()

    statement = Statement.query.filter(Statement.statement_number.not_in(answered)).order_by(Statement.statement_number).first()

    if not statement:
        return {}

    response = {
        "statement_number": statement.statement_number,
        "statement_choices": [
            {"choice_number": 1, "choice_text": statement.choice_1_text},
            {"choice_number": 2, "choice_text": statement.choice_2_text}
        ]
    }
    return jsonify(response)


@bp.route('/student/<student_number>/answer', methods=['POST'])
def submit_answer(student_number):
    student = Student.query.filter_by(student_number=student_number).first()
    if not student:
        return {"error": "Student not found."}, 404

    data = request.get_json()

    statement_number = data.get('statement_number')
    choice_number = data.get('choice_number')

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

    return {"message": "✅ Answer saved!"}, 201

