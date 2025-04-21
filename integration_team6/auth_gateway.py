from flask import Flask, request, jsonify
import requests
from login import authenticate_user_and_role

app = Flask(__name__)

# Feedback submission permissions by role
submission_permissions = {
    "/submit-student-feedback": "faculty",
    "/submit-prof-feedback": "student",
    "/submit-course-feedback": "faculty",
}

# Admin-only display endpoints
admin_display_routes = [
    "/feedback-count/course",
    "/feedback-count/faculty",
    "/top-courses",
    "/least-feedback-courses",
    "/most-active-faculty",
    "/recent-feedback",
    "/admin/generate-timetable",
    "/admin/dashboard",
    "/admin/add-notice",
]

# ------------------------------------------
# Feedback Submission Handlers (POST)
# ------------------------------------------
def forward_post_if_authorized(route_path):
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Missing credentials"}), 400

    role = authenticate_user_and_role(username, password)
    required_role = submission_permissions.get(route_path)

    if not role:
        return jsonify({"message": "Unauthorized"}), 401

    if required_role != role:
        return jsonify({"message": f"{role.capitalize()}s are not allowed to access this route"}), 403

    # Strip auth data before forwarding
    data.pop("username", None)
    data.pop("password", None)

    try:
        res = requests.post(f"http://host.docker.internal:5000{route_path}", json=data)
        return res.content, res.status_code, res.headers.items()
    except Exception as e:
        return jsonify({"message": f"Error contacting feedback service: {e}"}), 502


@app.route("/proxy/submit-student-feedback", methods=["POST"])
def proxy_submit_student_feedback():
    return forward_post_if_authorized("/submit-student-feedback")

@app.route("/proxy/submit-prof-feedback", methods=["POST"])
def proxy_submit_prof_feedback():
    return forward_post_if_authorized("/submit-prof-feedback")

@app.route("/proxy/submit-course-feedback", methods=["POST"])
def proxy_submit_course_feedback():
    return forward_post_if_authorized("/submit-course-feedback")

# ------------------------------------------
# Role-check helper for GET requests
# ------------------------------------------
def get_auth_role():
    username = request.args.get("username")
    password = request.args.get("password")

    if not username or not password:
        return None, jsonify({"message": "Missing credentials"}), 400

    role = authenticate_user_and_role(username, password)
    if not role:
        return None, jsonify({"message": "Unauthorized"}), 401

    return role, None, None

# ------------------------------------------
# Student View (Only Their Own)
# ------------------------------------------
@app.route("/proxy/feedback/<user_id>", methods=["GET"])
def proxy_display_feedback(user_id):
    username = request.args.get("username")
    role, error_response, status = get_auth_role()
    if error_response:
        return error_response, status

    if role != "student":
        return jsonify({"message": "Only students can access this route"}), 403

    if username != user_id:
        return jsonify({"message": "Students can only access their own feedback"}), 403

    try:
        res = requests.get(f"http://host.docker.internal:5001/feedback/{user_id}")
        return res.content, res.status_code, res.headers.items()
    except Exception as e:
        return jsonify({"message": f"Error contacting display service: {e}"}), 502

# ------------------------------------------
# Faculty View Feedback
# ------------------------------------------
@app.route("/proxy/view-feedback", methods=["GET"])
def proxy_view_feedback():
    role, error_response, status = get_auth_role()
    if error_response:
        return error_response, status

    if role != "faculty":
        return jsonify({"message": "Only faculty can access this route"}), 403

    try:
        res = requests.get("http://host.docker.internal:5001/view-feedback")
        return res.content, res.status_code, res.headers.items()
    except Exception as e:
        return jsonify({"message": f"Error contacting display service: {e}"}), 502

# ------------------------------------------
# Admin-only Display Analytics
# ------------------------------------------
def admin_get_proxy(path):
    role, error_response, status = get_auth_role()
    if error_response:
        return error_response, status

    if role != "admin":
        return jsonify({"message": "Admin access required"}), 403

    try:
        res = requests.get(f"http://host.docker.internal:5004{path}")
        return res.content, res.status_code, res.headers.items()
    except Exception as e:
        return jsonify({"message": f"Error contacting display service: {e}"}), 502

@app.route("/proxy/feedback-count/course", methods=["GET"])
def proxy_feedback_count_course():
    return admin_get_proxy("/feedback-count/course")

@app.route("/proxy/feedback-count/faculty", methods=["GET"])
def proxy_feedback_count_faculty():
    return admin_get_proxy("/feedback-count/faculty")

@app.route("/proxy/top-courses", methods=["GET"])
def proxy_top_courses():
    return admin_get_proxy("/top-courses")

@app.route("/proxy/least-feedback-courses", methods=["GET"])
def proxy_least_feedback_courses():
    return admin_get_proxy("/least-feedback-courses")

@app.route("/proxy/most-active-faculty", methods=["GET"])
def proxy_most_active_faculty():
    return admin_get_proxy("/most-active-faculty")

@app.route("/proxy/recent-feedback", methods=["GET"])
def proxy_recent_feedback():
    return admin_get_proxy("/recent-feedback")

@app.route("/proxy/admin/generate-timetable", methods=["GET"])
def proxy_generate_timetable():
    return admin_get_proxy("/admin/generate-timetable")

@app.route("/proxy/admin/dashboard", methods=["GET"])
def proxy_admin_dashboard():
    return admin_get_proxy("/admin/dashboard")


# ------------------------------------------
# Health Check
# ------------------------------------------
@app.route('/')
def root():
    return jsonify({"message": "Auth Gateway is running"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
