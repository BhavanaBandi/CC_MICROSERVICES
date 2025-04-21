from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    student_year = db.Column(db.Integer, nullable=False)
    student_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    feedbacks = db.relationship('Feedback', backref='student', lazy=True, foreign_keys='Feedback.student_id')

class Teacher(db.Model):
    teacher_id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(100), nullable=False)
    teacher_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    subjects = db.relationship('Subject', backref='teacher', lazy=True)
    feedbacks = db.relationship('Feedback', backref='teacher', lazy=True, foreign_keys='Feedback.teacher_id')

class Subject(db.Model):
    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(100), nullable=False)
    subject_year = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'), nullable=False)

class Timetable(db.Model):
    timetable_id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer)
    period = db.Column(db.Integer)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'))
    year = db.Column(db.Integer)

class Attendance(db.Model):
    attendance_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)

class Feedback(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True)
    feedback_text = db.Column(db.Text, nullable=False)
    feedback_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending')
    admin_response = db.Column(db.Text, nullable=True)
    user_role = db.Column(db.String(20), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'), nullable=True)

class Notice(db.Model):
    notice_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
