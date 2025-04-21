from app import app
from models import db, User, Student, Teacher, Subject

with app.app_context():
    db.drop_all()
    db.create_all()

    admin1 = User(username='admin1', password='pass', role='admin')
    admin2 = User(username='admin2', password='pass', role='admin')
    db.session.add_all([admin1, admin2])
    db.session.commit()

    teachers = []
    for i in range(1, 5):
        teacher_user = User(username=f'teacher{i}', password='pass', role='teacher')
        db.session.add(teacher_user)
        db.session.commit()

        teacher = Teacher(teacher_name=f'Teacher {i}', teacher_user_id=teacher_user.user_id)
        db.session.add(teacher)
        db.session.commit()
        teachers.append(teacher)

    for i in range(1, 21):
        student_user = User(username=f'student{i}', password='pass', role='student')
        db.session.add(student_user)
        db.session.commit()

        student = Student(
            student_name=f'Student {i}',
            student_year=(i % 4) + 1,
            student_user_id=student_user.user_id
        )
        db.session.add(student)

    db.session.commit()

    subjects = [
        Subject(subject_name='Mathematics', subject_year=1, teacher_id=teachers[0].teacher_id),
        Subject(subject_name='History', subject_year=1, teacher_id=teachers[1].teacher_id),
        Subject(subject_name='English', subject_year=1, teacher_id=teachers[2].teacher_id),
        Subject(subject_name='Science', subject_year=1, teacher_id=teachers[3].teacher_id),
        Subject(subject_name='Physics', subject_year=2, teacher_id=teachers[0].teacher_id),
        Subject(subject_name='Geography', subject_year=2, teacher_id=teachers[1].teacher_id),
        Subject(subject_name='Literature', subject_year=2, teacher_id=teachers[2].teacher_id),
        Subject(subject_name='Env Sci', subject_year=2, teacher_id=teachers[3].teacher_id),
        Subject(subject_name='Chemistry', subject_year=3, teacher_id=teachers[0].teacher_id),
        Subject(subject_name='CS', subject_year=3, teacher_id=teachers[1].teacher_id),
        Subject(subject_name='Economics', subject_year=3, teacher_id=teachers[2].teacher_id),
        Subject(subject_name='Social', subject_year=3, teacher_id=teachers[3].teacher_id),
        Subject(subject_name='Biology', subject_year=4, teacher_id=teachers[0].teacher_id),
        Subject(subject_name='Philosophy', subject_year=4, teacher_id=teachers[1].teacher_id),
        Subject(subject_name='Art', subject_year=4, teacher_id=teachers[2].teacher_id),
        Subject(subject_name='Adv Math', subject_year=4, teacher_id=teachers[3].teacher_id),
    ]

    db.session.add_all(subjects)
    db.session.commit()

    print("✅ Database initialized!")
