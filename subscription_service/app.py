from flask import Flask, request, jsonify
from subscriptions_functions import create_subscription, create_payment,complete_payment

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Parking Subscription and payment  service is running"})

@app.route("/create-subscription", methods=["POST"])
def create_subscription_route():
    data = request.get_json()
    user_id = data.get("user_id")
    plan_type = data.get("plan_type")

    response, status_code = create_subscription(user_id, plan_type)
    return jsonify(response), status_code

@app.route("/create-payment", methods=["POST"])
def create_payment_route():
    data = request.get_json()
    user_id = data.get("user_id")
    sub_id = data.get("sub_id")
    amount = data.get("amount")

    response, status_code = create_payment(user_id, sub_id, amount)
    return jsonify(response), status_code

@app.route("/complete-payment", methods=["POST"])
def complete_payment_route():
    data = request.get_json()
    user_id = data.get("user_id")

    response, status_code = complete_payment(user_id)
    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)