from flask import Flask, request, jsonify
from vehicle_functions import register_vehicle,update_registration,remove_vehicle, check_vehicle

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Vehicle details service is running"})

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    required_fields = ["user_id", "vehicle_number", "vehicle_type"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    result, status = register_vehicle(data["user_id"], data["vehicle_number"], data["vehicle_type"])
    return jsonify(result), status

@app.route("/update", methods=["PUT"])
def update():
    data = request.json
    required_fields = ["user_id", "cur_vehicle_number", "new_vehicle_number", "new_vehicle_type"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    result, status = update_registration(
        data["user_id"],
        data["cur_vehicle_number"],
        data["new_vehicle_number"],
        data["new_vehicle_type"]
    )
    return jsonify(result), status

@app.route("/remove", methods=["DELETE"])
def remove():
    user_id = request.args.get("user_id")
    vehicle_number = request.args.get("vehicle_number")

    if not user_id or not vehicle_number:
        return jsonify({"error": "Missing required fields"}), 400

    result, status = remove_vehicle(user_id,vehicle_number)
    return jsonify(result), status

@app.route("/check-vehicle", methods=["GET"])
def check_vehicle_route():
    vehicle_number = request.args.get("vehicle_number")

    if not vehicle_number:
        return jsonify({"error": "Missing vehicle_number parameter"}), 400

    result, status = check_vehicle(vehicle_number)
    return jsonify(result), status

    

if __name__ == "__main__":
    app.run(port=5000,debug=True, host="0.0.0.0")
