from flask import Flask, request, jsonify
import datetime
import json


app = Flask(__name__)

@app.route('/api2-process', methods=['POST'])
def api2_process():
    print(f"API2 LOG: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Received POST request from API 1 on /api2-process.")
    print(f"API2 LOG: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Caller IP: {request.remote_addr}")

    if not request.is_json:
        print(f"API2 ERROR: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Request from API 1 must be JSON. Content-Type was: {request.content_type}")
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    data_from_api1 = request.get_json()
    # คาดหวังฟิลด์ 'received_text_from_api1' ตามที่ API 1 ส่งมา
    received_text = data_from_api1.get('received_text_from_api1', 'No text received from API 1')

    # สร้าง Response ที่โต้ตอบกับข้อมูลที่ได้รับ
    response_data = {
        "message": f"API 2 received your message: '{received_text}'",
        "processed_at_api2": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "your_input_was": received_text,
        "api_name": "API 2 Responder"
    }
    print(f"API2 LOG: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sending response back to API 1: {json.dumps(response_data, ensure_ascii=False)}")
    return jsonify(response_data), 200

# Endpoint สำหรับทดสอบง่ายๆ
@app.route('/api2-status', methods=['GET'])
def api2_status():
    print(f"API2 LOG: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Received GET request on /api2-status. Responding directly.")
    return "API 2 is up and running! Send POST to /api2-process", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)