import mysql.connector
import os
from datetime import datetime, timedelta
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

def create_subscription(user_id, plan_type):
    try:
        conn,cursor=connect_mysql()

        cursor.execute("SELECT * FROM subscriptions WHERE user_id = %s AND end_date > DATE(NOW())", (user_id,))
        subs = cursor.fetchone()

        if subs:
            return {"message": "You already have an active subscription", "subscription": subs}, 400

        amount = 500.00 if plan_type.lower() == "monthly" else 5000.00
        start_date = datetime.today().date()
        end_date = start_date + timedelta(days=30 if plan_type.lower() == "monthly" else 365)

        cursor.execute("""
            INSERT INTO subscriptions (user_id, plan_type, amount, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, plan_type.lower(), amount, start_date, end_date))
        conn.commit()
        sub_id = cursor.lastrowid

        payload = {
            "user_id": user_id,
            "sub_id": sub_id,
            "amount": amount
        }
        payment_response = requests.post("http://subscription_service:5000/create-payment", json=payload)

        if payment_response.status_code != 200:
            return {"message": "Subscription created but failed to initialize payment"}, 500

        return {
            "message": "Subscription created successfully",
            "subscription_id": sub_id
        }, 200

    except mysql.connector.Error as err:
        return {"error": str(err)}, 500

    finally:
        cursor.close()
        conn.close()


def create_payment(user_id, sub_id, amount):
    try:
        conn,cursor=connect_mysql()

        cursor.execute("""
            INSERT INTO payments (user_id, sub_id, amount, status, payment_date)
            VALUES (%s, %s, %s, 'pending', NOW())
        """, (user_id, sub_id, amount))
        conn.commit()

        return {
            "message": "Payment initialized",
            "payment_id": cursor.lastrowid
        }, 200

    except mysql.connector.Error as err:
        return {"error": str(err)}, 500

    finally:
        cursor.close()
        conn.close()



def complete_payment(user_id):
    try:
        conn,cursor=connect_mysql()

        cursor.execute("""
            SELECT payment_id 
            FROM payments 
            WHERE user_id = %s AND status = 'pending' 
            ORDER BY payment_date DESC 
            LIMIT 1
        """, (user_id,))
        result = cursor.fetchone()

        if not result:
            return {"message": "No pending payments found"}, 404

        payment_id = result["payment_id"]

        cursor.execute("""
            UPDATE payments 
            SET status = 'completed', payment_date = NOW() 
            WHERE payment_id = %s
        """, (payment_id,))
        conn.commit()

        return {"message": f"Payment {payment_id} marked as completed"}, 200

    except mysql.connector.Error as err:
        return {"error": str(err)}, 500

    finally:
        cursor.close()
        conn.close()
