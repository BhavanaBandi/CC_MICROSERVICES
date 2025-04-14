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

def register_vehicle(user_id, vehicle_number, vehicle_type):
    try:
        conn, cursor= connect_mysql()
        print("connected")
        cursor.execute("SELECT role FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            return {"error": "User not found!"}, 404

        role = user["role"]
        max_vehicles = 1 if role == 'student' else 2
        cursor.execute("SELECT COUNT(*) as reg_count FROM vehicles WHERE user_id = %s", (user_id,))
        registered_count = cursor.fetchone()["reg_count"]
        if registered_count >= max_vehicles:
            return {
                "error": f"{role.capitalize()}s can register only {max_vehicles} vehicle(s).",
                "registered": registered_count
            }, 403

        if vehicle_type not in ['2 wheeler', '4 wheeler']:
            return {"error": "Invalid vehicle type. Must be '2 wheeler' or '4 wheeler'."}, 400

        # Check if vehicle already registered
        cursor.execute("SELECT * FROM vehicles WHERE vehicle_number = %s", (vehicle_number,))
        exists = cursor.fetchone()
        if exists:
            return {"error": "Vehicle already registered."}, 409

        # Insert vehicle
        cursor.execute("INSERT INTO vehicles (user_id, vehicle_number, vehicle_type) VALUES (%s, %s, %s)",(user_id, vehicle_number, vehicle_type))
        conn.commit()

        return {
            "message": f"Vehicle '{vehicle_number}' registered successfully as '{vehicle_type}'!",
            "user_id": user_id,
            "vehicle_number": vehicle_number,
            "vehicle_type": vehicle_type
        }, 201

    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}, 500

    finally:
        if cursor: 
            cursor.close()
        if conn: 
            conn.close()


def check_vehicle(vehicle_number):
    try:
        conn, cursor= connect_mysql()

        cursor.execute("SELECT user_id, vehicle_number, vehicle_type FROM vehicles WHERE vehicle_number = %s", (vehicle_number,))
        vehicle = cursor.fetchone()

        if not vehicle:
            return {"error": "Vehicle not found"}, 404

        return {"vehicle":vehicle}, 200

    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}, 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_registration(user_id, cur_vehicle_number, new_vehicle_number, new_vehicle_type):
    try:
        conn, cursor= connect_mysql()

        # Check if current vehicle exists and belongs to user
        cursor.execute("SELECT * FROM vehicles WHERE vehicle_number = %s AND user_id = %s", (cur_vehicle_number, user_id))
        vehicle = cursor.fetchone()

        if not vehicle:
            return {
                "error": f"No vehicle with number {cur_vehicle_number} found for user ID {user_id}. Update failed."
            }, 404

        # Check if new vehicle number already exists in the system
        cursor.execute("SELECT * FROM vehicles WHERE vehicle_number = %s", (new_vehicle_number,))
        duplicate = cursor.fetchone()

        if duplicate:
            return {
                "error": f"Vehicle with number {new_vehicle_number} already exists. Choose a different number."
            }, 409

        # Update registration
        cursor.execute(
            "UPDATE vehicles SET vehicle_number = %s, vehicle_type = %s WHERE vehicle_number = %s",
            (new_vehicle_number, new_vehicle_type, cur_vehicle_number)
        )
        conn.commit()

        return {
            "message": f"Vehicle {cur_vehicle_number} updated successfully to {new_vehicle_number} ({new_vehicle_type}).",
            "updated_vehicle": {
                "old_number": cur_vehicle_number,
                "new_number": new_vehicle_number,
                "new_type": new_vehicle_type
            }
        }, 200

    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}, 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def remove_vehicle(user_id, vehicle_number):
    try:
        conn, cursor= connect_mysql()

        cursor.execute("SELECT * FROM vehicles WHERE vehicle_number = %s AND user_id = %s", (vehicle_number, user_id))
        vehicle = cursor.fetchone()

        if not vehicle:
            return {"error": f"No vehicle found with number {vehicle_number} for user {user_id}."}, 404

        cursor.execute("DELETE FROM vehicles WHERE vehicle_number = %s", (vehicle_number,))
        conn.commit()

        return {
            "message": f"Vehicle {vehicle_number} removed successfully!",
            "vehicle_number": vehicle_number,
            "user_id": user_id
        }, 200

    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}, 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

