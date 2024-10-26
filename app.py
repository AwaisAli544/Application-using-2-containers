from flask import Flask, request, jsonify
import mysql.connector
import joblib
import datetime
import os

app = Flask(__name__)

# Load the pre-trained ML model
model = joblib.load('model/model_file.pkl')

# MySQL Database connection
def db_connection():
    conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'db'),  # Default to 'db' if not found
        user=os.getenv('MYSQL_USER', 'user'),
        password=os.getenv('MYSQL_PASSWORD', 'userpassword'),
        database=os.getenv('MYSQL_DATABASE', 'Model_Logger')
    )
    return conn

@app.route('/')
def home():
    return "Welcome to the ML Serving API!"


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_params = data['input_params']
    input_height = np.array(input_params).reshape(-1, 1)  # Ensure correct shape

    # Generate prediction
    prediction = model.predict(input_height)[0]

    # Log to database
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Log (Current_Date_Time, Input_Params, Output) VALUES (%s, %s, %s)",
        (datetime.datetime.now(), str(input_params), prediction)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'input_params': input_params, 'output': prediction})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8005)

