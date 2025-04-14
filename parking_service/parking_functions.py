import mysql.connector
import requests

def connect_mysql():
    conn = mysql.connector.connect(
            host="db",
            user="root",
            password="ijwtbpoys",
            database="university_db"
        )
    cursor = conn.cursor(dictionary=True)

    return conn, cursor

def get_available_parking_slots(slot_type):
    valid_types = ['all', '2 wheeler', '4 wheeler']
    if slot_type not in valid_types:
        return {"error": "Invalid slot type. Must be one of: all, 2 wheeler, 4 wheeler"}

    try:
        conn, cursor=connect_mysql()

        if slot_type == 'all':
            query = """
                SELECT type, location, COUNT(*) as count 
                FROM parking_slots 
                WHERE slot_status = 'available' 
                GROUP BY location, type;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
        else:
            query = """
                SELECT slot_id, location 
                FROM parking_slots 
                WHERE slot_status = 'available' AND type = %s 
                LIMIT 1;
            """
            cursor.execute(query, (slot_type,))
            result = cursor.fetchone()

        return result

    except mysql.connector.Error as err:
        return {"error": f"Database connection failed: {err} hello"}

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def assign_parking_slot(vehicle_number):
    try:
        conn, cursor=connect_mysql()

        response = requests.get("http://vehicle_service:5000/check-vehicle", params={"vehicle_number": vehicle_number})
        vehicle = response.json().get("vehicle")
        if not vehicle:
            return {"message": f"No vehicle found with number {vehicle_number}."}, 404

        slot_type = vehicle.get("vehicle_type")
        cursor.execute("SELECT * FROM assigned_slots WHERE vehicle_number = %s AND status = 'active'", (vehicle_number,))
        if cursor.fetchone():
            return {"message": "Vehicle is already assigned a slot."}, 400

        try:
            response = requests.get("http://parking_service:5000/available_slots", params={"type": slot_type})
            if response.status_code != 200:
                return {"error": f"Get slots service failed: {response.text}"}, 502
           
            available_slots = response.json()

            if not available_slots:
                return {"message": f"No available {slot_type} parking slots."}, 404

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to contact get_slots service: {e}"}, 503

        parking_slot = available_slots["slot_id"]
        location = available_slots["location"]

        cursor.execute("INSERT INTO assigned_slots (slot_id, vehicle_number) VALUES (%s, %s)",(parking_slot, vehicle_number))
        cursor.execute("UPDATE parking_slots SET slot_status = 'occupied' WHERE slot_id = %s",(parking_slot,))
        conn.commit()

        return {
            "message": f"Vehicle {vehicle_number} assigned to slot {parking_slot} at {location}.",
            "details": {
                "slot_id": parking_slot,
                "location": location,
                "vehicle_number": vehicle_number
            }
        }, 200

    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}, 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def unassign_parking(vehicle_number):
    try:
        conn, cursor=connect_mysql()

        cursor.execute("SELECT * FROM assigned_slots WHERE vehicle_number = %s AND status = 'active'", (vehicle_number,))
        assignment = cursor.fetchone()

        if not assignment:
            return { "message": f"No active parking assignment found for vehicle {vehicle_number}."}, 404
        
        assign_id, slot_id = assignment['assign_id'],assignment['slot_id']

        cursor.execute("UPDATE assigned_slots SET released_timestamp = NOW(), status = 'released' WHERE assign_id = %s",(assign_id,))
        cursor.execute("UPDATE parking_slots SET slot_status = 'available' WHERE slot_id = %s",(slot_id,))
        conn.commit()

        return {
            "message": f"Vehicle {vehicle_number} successfully unassigned from parking slot {slot_id}.",
            "details": {
                "vehicle_number": vehicle_number,
                "slot_id": slot_id,
                "status": "released"
            }
        }, 200

    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}, 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_history(history_type, start_date, end_date, user_id=None):
    try:
        conn, cursor=connect_mysql()

        history_type = history_type.lower()
        if history_type == 'all':
            query = """
                SELECT * FROM assigned_slots a
                JOIN parking_slots p ON a.slot_id = p.slot_id
                WHERE DATE(a.assigned_timestamp) >= %s AND DATE(a.assigned_timestamp) <= %s
            """
            params = (start_date, end_date)

        elif history_type == 'user':
            if not user_id:
                return {"error": "Missing user_id for user-specific history"}
            query = """
                SELECT * FROM assigned_slots a
                JOIN parking_slots p ON a.slot_id = p.slot_id
                JOIN vehicles v ON a.vehicle_number = v.vehicle_number
                WHERE DATE(a.assigned_timestamp) >= %s AND DATE(a.assigned_timestamp) <= %s
                AND v.user_id = %s
            """
            params = (start_date, end_date, user_id)

        else:
            return {"error": "Invalid history type. Use 'all' or 'user'."}

        cursor.execute(query, params)
        history = cursor.fetchall()



        return history if history else {"message": "No records found."}

    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

