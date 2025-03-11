from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database connection parameters
DB_HOST = os.getenv("DB_HOST", "postgres-service")
DB_NAME = os.getenv("POSTGRES_DB", "flask_webapp")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/")
def home():
    return jsonify({"message": "Flask app running on Kubernetes!"})

@app.route("/users")
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        conn.close()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)