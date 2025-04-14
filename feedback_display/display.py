# feedback_queries.py
import mysql.connector

def get_db_cursor():
    conn = mysql.connector.connect(
            host="db",
            user="root",
            password="ijwtbpoys",
            database="university_db"
        )
    cursor = conn.cursor()

    return conn, cursor

def display_feedback(user_id):
    feedback_data = {"role": None, "received": [], "given": []}

    try:
        conn,cursor=get_db_cursor()

        def get_user_type(uid):
            cursor.execute("SELECT stu_id FROM student WHERE stu_id = %s", (uid,))
            if cursor.fetchone():
                return "student"

            cursor.execute("SELECT prof_id FROM professor WHERE prof_id = %s", (uid,))
            if cursor.fetchone():
                return "professor"

            return None

        role = get_user_type(user_id)
        feedback_data["role"] = role

        if role == "student":
            # Feedback received
            cursor.execute("SELECT feedback_given_by_prof, time_of_feed_prof FROM prof_feedback WHERE stu_id = %s", (user_id,))
            feedback_data["received"] = cursor.fetchall()

            # Feedback given
            cursor.execute("SELECT prof_id, feedback_given_by_student, time_of_feed_stu FROM stu_feedback WHERE stu_id = %s", (user_id,))
            feedback_data["given"] = cursor.fetchall()

        elif role == "professor":
            # Feedback received
            cursor.execute("SELECT feedback_given_by_student, time_of_feed_stu FROM stu_feedback WHERE prof_id = %s", (user_id,))
            feedback_data["received"] = cursor.fetchall()

            # Feedback given
            cursor.execute("SELECT stu_id, feedback_given_by_prof, time_of_feed_prof FROM prof_feedback WHERE prof_id = %s", (user_id,))
            feedback_data["given"] = cursor.fetchall()

        return feedback_data

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"error": str(err)}

    finally:
        cursor.close()
        conn.close()

def view_feedback():
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT faculty_id, course_id, feedback_text, timestamp FROM course_feedback ORDER BY timestamp DESC")
    feedbacks = cursor.fetchall()
    conn.close()
    return [{"faculty_id": f[0], "course_id": f[1], "feedback": f[2], "timestamp": f[3].strftime("%Y-%m-%d %H:%M:%S")} for f in feedbacks]

def feedback_count_by_course():
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT course_id, COUNT(*) FROM course_feedback GROUP BY course_id")
    results = cursor.fetchall()
    conn.close()
    return [{"course_id": r[0], "feedback_count": r[1]} for r in results]

def feedback_count_by_faculty():
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT faculty_id, COUNT(*) FROM course_feedback GROUP BY faculty_id")
    results = cursor.fetchall()
    conn.close()
    return [{"faculty_id": r[0], "feedback_count": r[1]} for r in results]

def top_courses():
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT course_id, COUNT(*) AS feedback_count FROM course_feedback GROUP BY course_id ORDER BY feedback_count DESC LIMIT 5")
    results = cursor.fetchall()
    conn.close()
    return [{"course_id": r[0], "feedback_count": r[1]} for r in results]

def least_feedback_courses():
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT course_id, COUNT(*) AS feedback_count FROM course_feedback GROUP BY course_id ORDER BY feedback_count ASC LIMIT 5")
    results = cursor.fetchall()
    conn.close()
    return [{"course_id": r[0], "feedback_count": r[1]} for r in results]

def most_active_faculty():
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT faculty_id, COUNT(*) FROM course_feedback GROUP BY faculty_id ORDER BY COUNT(*) DESC LIMIT 5")
    results = cursor.fetchall()
    conn.close()
    return [{"faculty_id": r[0], "feedback_count": r[1]} for r in results]

def recent_feedback():
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT faculty_id, course_id, feedback_text, timestamp FROM course_feedback ORDER BY timestamp DESC LIMIT 10")
    results = cursor.fetchall()
    conn.close()
    return [{"faculty_id": r[0], "course_id": r[1], "feedback": r[2], "timestamp": r[3].strftime("%Y-%m-%d %H:%M:%S")} for r in results]
