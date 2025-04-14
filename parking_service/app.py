from flask import Flask, request, jsonify
from parking_functions import get_available_parking_slots, assign_parking_slot, unassign_parking, get_history

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Parking slot manangement service is running"})

@app.route('/available-slots', methods=['GET'])
def available_slots():
    slot_type = request.args.get('type', 'all')
    slots = get_available_parking_slots(slot_type)
    if isinstance(slots, str): 
        return jsonify({"error": slots}), 400
    elif slots is None:
        return jsonify({"error": "Database error"}), 500
    return jsonify(slots), 200

@app.route("/assign-parking", methods=["POST"])
def assign_parking_route():
    data = request.get_json()
    vehicle_number = data.get("vehicle_number")

    if not vehicle_number:
        return jsonify({"error": "Vehicle number is required"}), 400

    result, status_code = assign_parking_slot(vehicle_number)
    return jsonify(result), status_code

@app.route("/unassign-parking", methods=["POST"])
def unassign_parking_route():
    data = request.get_json()
    vehicle_number = data.get("vehicle_number")

    if not vehicle_number:
        return jsonify({"error": "Vehicle number is required"}), 400

    result, status = unassign_parking(vehicle_number)
    return jsonify(result), status

@app.route("/history", methods=["GET"])
def history():
    history_type = request.args.get("type") 
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    user_id = request.args.get("user_id")
    
    if not (history_type and start_date and end_date):
        return jsonify({"error": "Missing required parameters"}), 400

    result = get_history(history_type, start_date, end_date, user_id)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)