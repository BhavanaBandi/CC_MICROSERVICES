from flask import Blueprint, render_template, request, redirect, session, url_for
from models import db, User, Student, Teacher, Subject, Timetable, Attendance, Notice
import random
import json

app_routes = Blueprint('app_routes', __name__)
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from models import db, User, Student, Teacher, Subject, Timetable, Attendance, Feedback
import random
import json
from datetime import datetime, timedelta

import random

from flask import Blueprint, render_template, request, redirect, session, url_for
from models import db, User, Student, Teacher, Subject, Timetable
import random

app_routes = Blueprint('app_routes', __name__)


# Adapted timetable generation function
def generate_timetable(year):
    # Fetch teachers and their subjects for the given year
    teachers = []
    subjects = Subject.query.filter_by(subject_year=year).all()
    for subject in subjects:
        teacher = Teacher.query.get(subject.teacher_id)
        teachers.append({
            "teacher_id": teacher.teacher_id,
            "teacher_name": teacher.teacher_name,
            "subject_id": subject.subject_id,
            "subject_name": subject.subject_name,
            "slot": random.choice(["A", "B"]),  # Randomly assign slot
            "Th": 6  # Assume each teacher can teach up to 6 periods
        })

    # Initialize a 6x6 timetable grid
    timetable = [[None for _ in range(6)] for _ in range(6)]
    random.shuffle(teachers)

    for i in range(6):  # periods
        for j in range(6):  # days
            if not timetable[j][i]:  # If the slot is empty
                for t in teachers:
                    if t["Th"] > 0:
                        if (i == 0 and t["slot"] == "A") or (i == 5 and t["slot"] == "B") or (0 < i < 5):
                            t["Th"] -= 1
                            timetable[j][i] = {
                                "subject_id": t["subject_id"],
                                "teacher_id": t["teacher_id"]
                            }
                            break

    # Save the generated timetable to the database
    for day, periods in enumerate(timetable):
        for period, entry in enumerate(periods):
            if entry:
                new_entry = Timetable(
                    day=day,
                    period=period,
                    subject_id=entry["subject_id"],
                    teacher_id=entry["teacher_id"],
                    year=year
                )
                db.session.add(new_entry)
    db.session.commit()

# Route to generate timetable
@app_routes.route('/admin/generate-timetable', methods=['POST'])
def generate_timetable_route():
    if session.get('role') != 'admin':
        return redirect(url_for('app_routes.home'))

    # Get all unique years from the Subject table
    years = db.session.query(Subject.subject_year).distinct().all()
    years = [year[0] for year in years]  # Extract years from tuples

    # Clear existing timetable entries for all years
    Timetable.query.delete()
    db.session.commit()

    # Generate timetables for each year
    for year in years:
        generate_timetable(year)

    return redirect(url_for('app_routes.admin_dashboard'))



@app_routes.route('/')
def home():
    return 'Server is working'

# Login route
@app_routes.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['user_id'] = user.user_id
        session['role'] = user.role

        if user.role == 'admin':
            return redirect(url_for('app_routes.admin_dashboard'))
        elif user.role == 'teacher':
            return 'Logged in as teacher successfully!'
        elif user.role == 'student':
            return redirect(url_for('app_routes.student_dashboard'))

    return 'Invalid credentials'

# Admin dashboard

@app_routes.route('/teacher/dashboard')
def teacher_dashboard():
    if session.get('role') != 'teacher':
        return redirect(url_for('app_routes.home'))

    # Get the logged-in teacher
    teacher = Teacher.query.filter_by(teacher_user_id=session.get('user_id')).first()

    # Get subjects taught by the teacher
    subjects = Subject.query.filter_by(teacher_id=teacher.teacher_id).all()

    # Extract subject IDs for querying the timetable
    subject_ids = [subject.subject_id for subject in subjects]

    # Get timetable entries for the teacher's subjects
    timetable_entries = Timetable.query.filter(Timetable.subject_id.in_(subject_ids)).all()

    # Organize timetable into a 6x6 grid (6 days x 6 periods)
    timetable_data = [[None for _ in range(6)] for _ in range(6)]
    for entry in timetable_entries:
        day = entry.day
        period = entry.period

        # Fetch subject details
        subject = Subject.query.get(entry.subject_id)

        timetable_data[day][period] = {
            "subject": subject.subject_name,
            "year": subject.subject_year
        }

    # Fetch students for each subject
    subject_students = {}
    for subject in subjects:
        students = Student.query.filter_by(student_year=subject.subject_year).all()
        subject_students[subject.subject_name] = students

    return render_template(
        'teacher_dashboard.html',
        teacher=teacher,
        subjects=subjects,
        timetable=timetable_data,
        subject_students=subject_students
    )

from datetime import datetime, timedelta

@app_routes.route('/teacher/attendance/<int:subject_id>', methods=['GET', 'POST'])
def attendance(subject_id):
    if session.get('role') != 'teacher':
        return redirect(url_for('app_routes.home'))

    # Get the logged-in teacher
    teacher = Teacher.query.filter_by(teacher_user_id=session.get('user_id')).first()

    # Get the subject
    subject = Subject.query.get(subject_id)
    if not subject or subject.teacher_id != teacher.teacher_id:
        return "Unauthorized", 403

    # Generate class dates for the year (assuming 10 weeks, 6 days/week)
    start_date = datetime(2023, 1, 1)  # Example start date
    class_dates = [start_date + timedelta(days=i) for i in range(10 * 6)]  # 10 weeks, 6 days/week

    # Fetch students for the subject's year
    students = Student.query.filter_by(student_year=subject.subject_year).all()

    if request.method == 'POST':
        # Process attendance submission
        date_str = request.form.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        for student in students:
            status = request.form.get(f'student_{student.student_id}')
            attendance_record = Attendance.query.filter_by(
                student_id=student.student_id,
                subject_id=subject_id,
                date=date
            ).first()

            if attendance_record:
                # Update existing record
                attendance_record.status = status
            else:
                # Create new record
                new_attendance = Attendance(
                    student_id=student.student_id,
                    subject_id=subject_id,
                    date=date,
                    status=status
                )
                db.session.add(new_attendance)

        db.session.commit()
        return redirect(url_for('app_routes.attendance', subject_id=subject_id))

    return render_template(
        'attendance.html',
        teacher=teacher,
        subject=subject,
        class_dates=class_dates,
        students=students
    )

# Student dashboard
from datetime import datetime, timedelta

@app_routes.route('/student/dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect(url_for('app_routes.home'))

    # Get the logged-in student
    student = Student.query.filter_by(student_user_id=session.get('user_id')).first()

    # Get subjects based on the student's year
    subjects = Subject.query.filter_by(subject_year=student.student_year).all()

    # Calculate attendance summary for each subject
    attendance_summary = []
    for subject in subjects:
        # Count total marked classes for the subject
        total_marked_classes = Attendance.query.filter_by(
            student_id=student.student_id,
            subject_id=subject.subject_id
        ).count()

        # Count present classes for the subject
        present_classes = Attendance.query.filter_by(
            student_id=student.student_id,
            subject_id=subject.subject_id,
            status="Present"
        ).count()

        attendance_summary.append({
            "subject_name": subject.subject_name,
            "present_classes": present_classes,
            "total_marked_classes": total_marked_classes
        })

    # Get timetable entries for the student's year
    timetable_entries = Timetable.query.filter_by(year=student.student_year).all()

    # Organize timetable into a 6x6 grid (6 days x 6 periods)
    timetable_data = [[None for _ in range(6)] for _ in range(6)]
    for entry in timetable_entries:
        day = entry.day
        period = entry.period

        # Fetch subject and teacher details
        subject = Subject.query.get(entry.subject_id)
        teacher = Teacher.query.get(entry.teacher_id)

        timetable_data[day][period] = {
            "subject": subject.subject_name,
            "teacher": teacher.teacher_name
        }

    return render_template(
        'student_dashboard.html',
        student=student,
        subjects=subjects,
        timetable=timetable_data,
        attendance_summary=attendance_summary
    )
@app_routes.route('/student/view-attendance/<string:subject_name>')
def view_attendance(subject_name):
    if session.get('role') != 'student':
        return redirect(url_for('app_routes.home'))

    # Get the logged-in student
    student = Student.query.filter_by(student_user_id=session.get('user_id')).first()

    # Get the subject
    subject = Subject.query.filter_by(subject_name=subject_name).first()
    if not subject:
        return "Subject not found", 404

    # Fetch attendance records for the student and subject
    attendance_records = Attendance.query.filter_by(
        student_id=student.student_id,
        subject_id=subject.subject_id
    ).order_by(Attendance.date).all()

    return render_template(
        'view_attendance.html',
        student=student,
        subject=subject,
        attendance_records=attendance_records
    )

# Logout
@app_routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('app_routes.home'))


@app_routes.route('/feedback', methods=['GET', 'POST'])
def feedback_form():
    user_id = session.get('user_id')
    role = session.get('role')
    
    if not user_id or role not in ['student', 'teacher']:
        return redirect(url_for('app_routes.home'))
    
    # Get the user based on role
    if role == 'student':
        user = Student.query.filter_by(student_user_id=user_id).first()
        user_id_field = user.student_id
        user_name = user.student_name
    else:  # role == 'teacher'
        user = Teacher.query.filter_by(teacher_user_id=user_id).first()
        user_id_field = user.teacher_id
        user_name = user.teacher_name
    
    if request.method == 'POST':
        feedback_text = request.form.get('feedback_text')
        
        if feedback_text:
            # Create new feedback
            new_feedback = Feedback(
                feedback_text=feedback_text,
                feedback_date=datetime.utcnow(),
                status='Pending',
                user_role=role
            )
            
            # Set the appropriate ID based on role
            if role == 'student':
                new_feedback.student_id = user_id_field
            else:  # role == 'teacher'
                new_feedback.teacher_id = user_id_field
                
            db.session.add(new_feedback)
            db.session.commit()
            
            flash('Your feedback has been submitted successfully!', 'success')
            
            # Redirect based on role
            if role == 'student':
                return redirect(url_for('app_routes.student_dashboard'))
            else:  # role == 'teacher'
                return redirect(url_for('app_routes.teacher_dashboard'))
        else:
            flash('Feedback cannot be empty!', 'error')
    
    # Get existing feedback from this user
    if role == 'student':
        previous_feedbacks = Feedback.query.filter_by(student_id=user_id_field).order_by(Feedback.feedback_date.desc()).all()
    else:  # role == 'teacher'
        previous_feedbacks = Feedback.query.filter_by(teacher_id=user_id_field).order_by(Feedback.feedback_date.desc()).all()
    
    return render_template(
        'feedback_form.html',
        user_name=user_name,
        role=role,
        previous_feedbacks=previous_feedbacks
    )

# Separate routes to redirect to the unified form
@app_routes.route('/student/feedback')
def student_feedback():
    if session.get('role') != 'student':
        return redirect(url_for('app_routes.home'))
    return redirect(url_for('app_routes.feedback_form'))

@app_routes.route('/teacher/feedback')
def teacher_feedback():
    if session.get('role') != 'teacher':
        return redirect(url_for('app_routes.home'))
    return redirect(url_for('app_routes.feedback_form'))

# Route for admin to view all feedback
@app_routes.route('/admin/view-feedback')
def admin_view_feedback():
    if session.get('role') != 'admin':
        return redirect(url_for('app_routes.home'))
    
    # Get all feedback with user info
    student_feedback = db.session.query(
        Feedback, Student.student_name
    ).join(
        Student, Feedback.student_id == Student.student_id
    ).filter(
        Feedback.user_role == 'student'
    ).all()
    
    teacher_feedback = db.session.query(
        Feedback, Teacher.teacher_name
    ).join(
        Teacher, Feedback.teacher_id == Teacher.teacher_id
    ).filter(
        Feedback.user_role == 'teacher'
    ).all()
    
    # Format data for template
    student_feedback_data = [(f, name, 'Student') for f, name in student_feedback]
    teacher_feedback_data = [(f, name, 'Teacher') for f, name in teacher_feedback]
    
    # Combine and sort by date
    all_feedback = student_feedback_data + teacher_feedback_data
    all_feedback.sort(key=lambda x: x[0].feedback_date, reverse=True)
    
    return render_template(
        'admin_feedback.html',
        all_feedback=all_feedback
    )

# Route for admin to respond to feedback
@app_routes.route('/admin/respond-feedback/<int:feedback_id>', methods=['POST'])
def admin_respond_feedback(feedback_id):
    if session.get('role') != 'admin':
        return redirect(url_for('app_routes.home'))
    
    feedback = Feedback.query.get_or_404(feedback_id)
    response = request.form.get('admin_response')
    status = request.form.get('status')
    
    if response:
        feedback.admin_response = response
    
    if status:
        feedback.status = status
    
    db.session.commit()
    flash('Response submitted successfully!', 'success')
    return redirect(url_for('app_routes.admin_view_feedback'))

# Modify the existing admin_dashboard route to include a feedback button
@app_routes.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('app_routes.home'))

    # Fetch all students, teachers, and subjects
    students = Student.query.all()
    teachers = Teacher.query.all()
    subjects = Subject.query.all()

    # Count pending feedback
    pending_feedback_count = Feedback.query.filter_by(status='Pending').count()

    # Fetch all timetable entries
    timetable_entries = Timetable.query.all()

    # Organize timetable data by year
    timetables_by_year = {}
    for entry in timetable_entries:
        year = entry.year
        day = entry.day
        period = entry.period

        # Fetch subject and teacher details
        subject = Subject.query.get(entry.subject_id)
        teacher = Teacher.query.get(entry.teacher_id)

        if year not in timetables_by_year:
            timetables_by_year[year] = [[None for _ in range(6)] for _ in range(6)]

        timetables_by_year[year][day][period] = {
            "subject": subject.subject_name if subject else "N/A",
            "teacher": teacher.teacher_name if teacher else "N/A"
        }

    return render_template(
        'admin_dashboard.html',
        students=students,
        teachers=teachers,
        subjects=subjects,
        pending_feedback_count=pending_feedback_count,
        timetables_by_year=timetables_by_year
    )
@app_routes.route('/admin/add-notice', methods=['GET', 'POST'])
def add_notice():
    if session.get('role') != 'admin':
        return redirect(url_for('app_routes.home'))

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if title and content:
            new_notice = Notice(title=title, content=content)
            db.session.add(new_notice)
            db.session.commit()
            return redirect(url_for('app_routes.admin_dashboard'))

    return render_template('add_notice.html')

@app_routes.route('/view-notices')
def view_notices():
    # Fetch all notices in descending order of timestamp (latest first)
    notices = Notice.query.order_by(Notice.timestamp.desc()).all()

    # Filter out any None values (if they exist)
    notices = [notice for notice in notices if notice is not None]

    return render_template('view_notices.html', notices=notices)