from flask import Flask, request, jsonify
from display import display_feedback, view_feedback, feedback_count_by_course,feedback_count_by_faculty
from display import top_courses,least_feedback_courses,most_active_faculty,recent_feedback

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Feedback Display service is running"})

@app.route('/feedback/<user_id>', methods=['GET'])
def get_feedback(user_id):
    feedback = display_feedback(user_id)
    
    if feedback.get("error"):
        return jsonify({"error": feedback["error"]}), 500
    
    return jsonify(feedback)

@app.route("/view-feedback", methods=["GET"])
def route_view_feedback():
    return jsonify(view_feedback())

@app.route("/feedback-count/course", methods=["GET"])
def route_feedback_count_course():
    return jsonify(feedback_count_by_course())

@app.route("/feedback-count/faculty", methods=["GET"])
def route_feedback_count_faculty():
    return jsonify(feedback_count_by_faculty())

@app.route("/top-courses", methods=["GET"])
def route_top_courses():
    return jsonify(top_courses())

@app.route("/least-feedback-courses", methods=["GET"])
def route_least_feedback_courses():
    return jsonify(least_feedback_courses())

@app.route("/most-active-faculty", methods=["GET"])
def route_most_active_faculty():
    return jsonify(most_active_faculty())

@app.route("/recent-feedback", methods=["GET"])
def route_recent_feedback():
    return jsonify(recent_feedback())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
