import json
from app import create_app
from app.models import db, Student

app = create_app()

with app.app_context():    
    with open('data/students.json') as f:
        students = json.load(f)

    for student in students:
        new_student = Student(
            student_number=student['student_number'],
            name=student['student_name'],
            student_class=student['student_class']
        )
        db.session.add(new_student)

    db.session.commit()
    print(f"✅ Imported {len(students)} students!")



  
  