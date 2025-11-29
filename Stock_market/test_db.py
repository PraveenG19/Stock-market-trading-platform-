import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="user_auth"
    )
    cursor = conn.cursor()
    cursor.execute("SHOW COLUMNS FROM trading_history")
    result = cursor.fetchall()
    print("Trading history table structure:")
    for row in result:
        print(row)
    conn.close()
except Exception as e:
    print(f"Error: {e}")