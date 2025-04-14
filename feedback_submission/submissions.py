import mysql.connector

def connect_mysql():
    conn = mysql.connector.connect(
            host="db",
            user="root",
            password="ijwtbpoys",
            database="university_db"
        )
    cursor = conn.cursor(dictionary=True)

    return conn, cursor

def submit_student_feedback(stu_id,faculty_id,feedback):
    """
    Allows faculty to submit feedback for a student.
    """
    try:
        conn, cursor=connect_mysql()
        # Check if the faculty ID exists in the database
        cursor.execute("SELECT stu_id FROM student WHERE stu_id = %s", (stu_id,))

        if cursor.fetchone() is None:
            return {"message": f"Student with ID {stu_id} not found "}, 404
        
        # Check if the faculty ID exists in the database
        cursor.execute("SELECT prof_id FROM professor WHERE prof_id = %s", (faculty_id,))
        if cursor.fetchone() is None:
            return {"message": f"Professor with ID {faculty_id} not found "}, 404

        # Insert the feedback for the faculty
        query = """
            INSERT INTO prof_feedback (prof_id, stu_id, feedback_given_by_prof, time_of_feed_prof)
            VALUES (%s, %s, %s, NOW())
        """
        cursor.execute(query, (faculty_id, stu_id, feedback))
        conn.commit()
        return {"message": "Feedback submitted successfully."}, 201
        
    except mysql.connector.Error as err:
       
        return {"error": f"Database connection failed: {err} hello"},500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def submit_faculty_feedback(stu_id, faculty_id, feedback):
    try:
        conn, cursor=connect_mysql()
        # Check if the faculty ID exists in the database
        cursor.execute("SELECT prof_id FROM professor WHERE prof_id = %s", (faculty_id,))

        if cursor.fetchone() is None:
            print("Faculty doesn't exist")
            return {"message": f"Faculty with ID {faculty_id} not found "}, 404
        
        cursor.execute("SELECT stu_id FROM student WHERE stu_id = %s", (stu_id,))

        if cursor.fetchone() is None:
            return {"message": f"Student with ID {stu_id} not found "}, 404

        # Insert the feedback for the faculty
        query = """
            INSERT INTO stu_feedback (stu_id, prof_id, feedback_given_by_student, time_of_feed_stu)
            VALUES (%s, %s, %s, NOW())
        """
        cursor.execute(query, (stu_id, faculty_id, feedback))
        conn.commit()
        return {"message": "Feedback submitted successfully."}, 201
        
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        print("hello")
        return {"error": f"Database connection failed: {err} hello"},500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def submit_course_feedback(faculty_id,course_id,feedback_text):
    """
    Allows faculty to submit feedback for a course.
    """ 
    try:
        conn, cursor=connect_mysql()
        
        query = """
            INSERT INTO course_feedback (faculty_id, course_id, feedback_text, timestamp)
            VALUES (%s, %s, %s, NOW())
        """
        cursor.execute(query, (faculty_id, course_id, feedback_text))
        conn.commit()
        return {"message": "Feedback submitted successfully."}, 201
        
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        print("hello")
        return {"error": f"Database connection failed: {err} hello"}

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    