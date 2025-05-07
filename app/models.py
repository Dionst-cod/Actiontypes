from flask_sqlalchemy import SQLAlchemy
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

    def __repr__(self):
        return f"<Statement {self.statement_number}>"


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(10), db.ForeignKey('students.student_number'), nullable=False)
    statement_number = db.Column(db.Integer, db.ForeignKey('statements.statement_number'), nullable=False)
    choice_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Answer Student {self.student_number} - Statement {self.statement_number} - Choice {self.choice_number}>"

