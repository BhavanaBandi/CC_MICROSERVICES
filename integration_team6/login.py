import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='host.docker.internal',  # or 'db' if using Docker Compose
        user='root',
        password='Folklore@2004',
        database='microservices'
    )

def authenticate_user_and_role(user_id, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Student login
    cursor.execute("SELECT password FROM student_login WHERE username = %s", (user_id,))
    student = cursor.fetchone()
    if student and student['password'] == password:
        return 'student'

    # Faculty login
    cursor.execute("SELECT password FROM professor_login WHERE username = %s", (user_id,))
    prof = cursor.fetchone()
    if prof and prof['password'] == password:
        return 'faculty'

    # Admin login
    cursor.execute("SELECT password FROM admin_login WHERE username = %s", (user_id,))
    admin = cursor.fetchone()
    if admin and admin['password'] == password:
        return 'admin'

    return None
