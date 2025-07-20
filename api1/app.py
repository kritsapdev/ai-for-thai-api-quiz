import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ดึง URL ของ API 2 จาก environment variable
# ใน Docker Compose เราจะกำหนดค่านี้
API2_URL = os.getenv('API2_URL', 'http://api2:8001/api2-hello')

@app.route('/api1-hello', methods=['GET'])
def api1_hello():
    print(f"API1 LOG: Received GET request from user on /api1-hello.")
    print(f"API1 LOG: User IP: {request.remote_addr}")

    try:
        # ส่ง Request ไปยัง API 2
        print(f"API1 LOG: Forwarding request to API 2 at {API2_URL}...")
        response_from_api2 = requests.get(API2_URL)
        response_from_api2.raise_for_status() # ตรวจสอบว่า HTTP request สำเร็จหรือไม่

        api2_message = response_from_api2.text
        print(f"API1 LOG: Received response from API 2: \"{api2_message}\"")

        # เตรียมคำตอบที่จะส่งกลับไปยัง User
        final_response = {
            "message_from_api1": "Hello from API 1! (Request forwarded to API 2)",
            "message_from_api2": api2_message
        }
        print(f"API1 LOG: Sending final response back to user.")
        return jsonify(final_response), 200

    except requests.exceptions.ConnectionError as e:
        print(f"API1 ERROR: Could not connect to API 2 at {API2_URL}. Error: {e}")
        return jsonify({"status": "error", "message": "Failed to connect to API 2"}), 500
    except requests.exceptions.RequestException as e:
        print(f"API1 ERROR: An error occurred while communicating with API 2. Error: {e}")
        return jsonify({"status": "error", "message": f"Error from API 2: {e}"}), 500
    except Exception as e:
        print(f"API1 ERROR: An unexpected error occurred: {e}")
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    # รัน Flask app บนพอร์ต 8000
    app.run(host='0.0.0.0', port=8000)