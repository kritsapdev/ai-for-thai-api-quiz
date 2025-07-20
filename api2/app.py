from flask import Flask, request

app = Flask(__name__)

@app.route('/api2-hello', methods=['GET'])
def api2_hello():
    print(f"API2 LOG: Received GET request from API 1 on /api2-hello.")
    print(f"API2 LOG: Caller IP: {request.remote_addr}")

    response_message = "Hello from API 2!"
    print(f"API2 LOG: Sending response back to API 1: \"{response_message}\"")
    return response_message, 200

if __name__ == '__main__':
    # รัน Flask app บนพอร์ต 8001
    app.run(host='0.0.0.0', port=8001)