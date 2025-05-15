from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    student_class = db.Column(db.String(50), nullable=False)
    team = db.Column(db.String(50), nullable=True)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Student {self.student_number} - {self.name}>"
    

class Statement(db.Model):
    __tablename__ = 'statements'

    id = db.Column(db.Integer, primary_key=True)
    statement_number = db.Column(db.Integer, nullable=False)
    choice_1_text = db.Column(db.String(255), nullable=False)
    choice_2_text = db.Column(db.String(255), nullable=False)
    trait_type = db.Column(db.String(2), nullable=False)  # e.g., 'EI', 'SN', etc.

    def __repr__(self):
        return f"<Statement {self.statement_number}>"


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(10), db.ForeignKey('students.student_number'), nullable=False)
    statement_number = db.Column(db.Integer, db.ForeignKey('statements.statement_number'), nullable=False)
    choice_number = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # ⬅️ Nieuw veld hier

    def __repr__(self):
        return f"<Answer Student {self.student_number} - Statement {self.statement_number} - Choice {self.choice_number}>"

class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
