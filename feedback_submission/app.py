from flask import Flask, request, jsonify
from submissions import submit_student_feedback,submit_faculty_feedback,submit_course_feedback

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": " Feedback submission service is running"})

@app.route("/submit-student-feedback", methods=["POST"])
def student_feedback():
    data = request.get_json()
    
    stu_id = data.get("stu_id")
    prof_id = data.get("prof_id")
    feedback = data.get("feedback")

    if not all([stu_id,prof_id,feedback]):
        return jsonify({"message": "Missing fields"}), 400
    
    response, status = submit_student_feedback(stu_id,prof_id,feedback)
    return jsonify(response), status

@app.route("/submit-prof-feedback", methods=["POST"])
def prof_feedback():
    data = request.get_json()

    stu_id = data.get("stu_id")
    prof_id = data.get("prof_id")
    feedback = data.get("feedback")

    if not all([stu_id,prof_id,feedback]):
        return jsonify({"message": "Missing fields"}), 400
    
    print(data)
    response, status = submit_faculty_feedback(stu_id, prof_id, feedback)
    return jsonify(response), status

@app.route("/submit-course-feedback", methods=["POST"])
def course_feedback():
    data = request.get_json()

    faculty_id = data.get("faculty_id")
    course_id = data.get("course_id")
    feedback = data.get("feedback")

    if not all([faculty_id, course_id, feedback]):
            return {"message": "Missing required fields"}, 400

    response, status = submit_course_feedback(faculty_id,course_id,feedback)
    return jsonify(response), status


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
