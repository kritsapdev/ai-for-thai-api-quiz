import os
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# ดึง URL ของ API 2 จาก environment variable
# ใน Docker Compose เราจะกำหนดค่านี้ (http://api2:8001/api2-process)
API2_URL = os.getenv('API2_URL', 'http://api2:8001/api2-process')

@app.route('/api1-process', methods=['POST'])
def api1_process():
    print(f"API1 LOG: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Received POST request from user on /api1-process.")
    print(f"API1 LOG: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] User IP: {request.remote_addr}")

    if not request.is_json:
        print(f"API1 ERROR: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Request must be JSON. Content-Type was: {request.content_type}")
        return jsonify({"status": "error", "message": "Request must be JSON. Please set Content-Type to application/json and send a valid JSON body."}), 400

    user_data = request.get_json()
    input_text = user_data.get('text', 'No text provided by user') # รับค่า 'text' จากผู้ใช้

    print(f"API1 LOG: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Received text from user: \"{input_text}\"")

    try:
        # ส่ง Request ไปยัง API 2 พร้อมกับข้อมูลที่ได้รับจากผู้ใช้
        print(f"API1 LOG: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Forwarding data to API 2 at {API2_URL}...")
        
        # ส่งข้อมูลเป็น JSON Body ไปยัง API 2
        response_from_api2 = requests.post(API2_URL, json={"received_text_from_api1": input_text}) 
        response_from_api2.raise_for_status() # ตรวจสอบว่า HTTP request สำเร็จหรือไม่ (2xx status)

        api2_response_json = response_from_api2.json() # คาดหวัง JSON response จาก API 2
        print(f"API1 LOG: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Received response from API 2: {json.dumps(api2_response_json, indent=2, ensure_ascii=False)}")

        # เตรียมคำตอบที่จะส่งกลับไปยัง User
        final_response = {
            "status": "success",
            "message_from_api1": "API 1 processed your request and got a response from API 2.",
            "original_text_sent_by_user": input_text,
            "response_from_api2": api2_response_json
        }
        print(f"API1 LOG: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sending final response back to user.")
        return jsonify(final_response), 200

    except requests.exceptions.ConnectionError as e:
        print(f"API1 ERROR: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Could not connect to API 2 at {API2_URL}. Error: {e}")
        return jsonify({"status": "error", "message": f"Failed to connect to API 2 at {API2_URL}. Please check if API 2 is running and accessible."}), 500
    except requests.exceptions.RequestException as e:
        print(f"API1 ERROR: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] An error occurred while communicating with API 2. Error: {e}")
        error_details = {"status_code": getattr(e.response, 'status_code', 'N/A'), "response_text": getattr(e.response, 'text', 'N/A')}
        print(f"API1 ERROR: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] API 2 responded with: {json.dumps(error_details, ensure_ascii=False)}")
        return jsonify({"status": "error", "message": f"Error from API 2: {e}", "details": error_details}), 500
    except Exception as e:
        print(f"API1 ERROR: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] An unexpected error occurred in API 1: {e}")
        return jsonify({"status": "error", "message": f"An unexpected error occurred in API 1: {e}"}), 500

# Endpoint สำหรับทดสอบง่ายๆ
@app.route('/api1-status', methods=['GET'])
def api1_status():
    print(f"API1 LOG: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Received GET request on /api1-status. Responding directly.")
    return "API 1 is up and running! Send POST to /api1-process", 200

if __name__ == '__main__':
    # เพิ่ม import datetime ที่ด้านบนสุดของไฟล์
    import datetime 
    app.run(host='0.0.0.0', port=8000)