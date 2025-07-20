# API Chaining with Docker Compose (2 Containers - Hello World)

โปรเจกต์นี้สาธิตการทำงานของ API สองตัวที่แยกกันอยู่คนละ Docker Container (API 1 และ API 2) และมีการเชื่อมโยงการทำงานระหว่างกัน: API 1 จะส่ง Request ไปยัง API 2 และนำคำตอบจาก API 2 กลับมาแสดงผลให้ผู้ใช้.

---

## คุณสมบัติ

* **API 1 (Gateway):** รับ GET Request ที่ `/api1-hello` จากผู้ใช้, พิมพ์ Log, ส่งต่อ Request ไปยัง API 2, พิมพ์ Log, รับคำตอบจาก API 2, พิมพ์ Log, และส่งคำตอบรวมกลับคืนให้ผู้ใช้
* **API 2 (Processor):** รับ GET Request ที่ `/api2-hello` จาก API 1, พิมพ์ Log, สร้างคำตอบ "Hello from API 2!", พิมพ์ Log, และส่งคำตอบกลับไปให้ API 1
* **ภาษาที่ใช้:** Python (Flask Framework)
* **การจัดการ Container:** Docker และ Docker Compose (ทำให้มี 2 Containers แยกกัน)
* **การบันทึก Log:** มีการ Print logs ทั้งบน API1 และ API2 เพื่อให้เห็น Workflow การทำงาน

---

## ความต้องการเบื้องต้น (Prerequisites)

* [**Docker Desktop**](https://www.docker.com/products/docker-desktop/) (รวม Docker Engine และ Docker Compose) ติดตั้งบนเครื่องของคุณ

---

## โครงสร้างโปรเจกต์

AI for thai hackaton
Custom Gem
เข้าใจเลยครับ! งั้นเราจะกลับไปที่โครงสร้างโปรเจกต์แบบ 2 Container เพื่อสาธิตการทำงานของ API 1 เรียก API 2 บน Docker Compose โดยมีเงื่อนไข "Hello World" เป็น Response ครับ

โปรเจกต์นี้จะประกอบด้วย:

API 1 (Gateway): รับ Request จากผู้ใช้, พิมพ์ Log, ส่ง Request ต่อไปยัง API 2, พิมพ์ Log, รับคำตอบจาก API 2, พิมพ์ Log, และส่งคำตอบกลับไปที่ผู้ใช้

API 2 (Processor): รับ Request จาก API 1, พิมพ์ Log, สร้างคำตอบ "Hello from API 2!", พิมพ์ Log, และส่งคำตอบกลับไปที่ API 1

โครงสร้างโปรเจกต์ (2 Containers)
เราจะจัดโครงสร้างไฟล์ดังนี้:

.
├── api1/
│   ├── app.py
│   └── requirements.txt
│   └── Dockerfile
├── api2/
│   ├── app.py
│   └── requirements.txt
│   └── Dockerfile
└── docker-compose.yml
└── README.md
1. โค้ดสำหรับ API 1 (api1/app.py)
นี่คือโค้ดสำหรับ API ตัวแรกที่จะรับ Request จากผู้ใช้ ส่งต่อไปยัง API 2 และส่งคำตอบกลับ:

Python

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
2. โค้ดสำหรับ API 2 (api2/app.py)
นี่คือโค้ดสำหรับ API ตัวที่สองที่จะรับ Request จาก API 1 และส่งคำตอบ "Hello from API 2!" กลับไป:

Python

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
3. ไฟล์ requirements.txt สำหรับแต่ละ API
api1/requirements.txt:

Flask==2.3.3
requests==2.31.0
api2/requirements.txt:

Flask==2.3.3
4. ไฟล์ Dockerfile สำหรับแต่ละ API
api1/Dockerfile:

Dockerfile

# ใช้ Python 3.9 slim-buster เพื่อให้ Image มีขนาดเล็กและเข้ากันได้กับ apt
FROM python:3.9-slim-buster

# ตั้งค่า Working directory ภายใน Container
WORKDIR /app

# คัดลอกไฟล์ requirements.txt ไปยัง Working directory
COPY requirements.txt .

# ติดตั้ง Python packages ที่ระบุใน requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์โค้ดของ API ทั้งหมดไปยัง Working directory
COPY app.py .

# กำหนดพอร์ตที่ Container จะเปิด (ตรงกับ app.run() ใน app.py)
EXPOSE 8000

# คำสั่งสำหรับรัน Flask app เมื่อ Container เริ่มต้น
CMD ["python", "app.py"]
api2/Dockerfile:

Dockerfile

# ใช้ Python 3.9 slim-buster
FROM python:3.9-slim-buster

# ตั้งค่า Working directory ภายใน Container
WORKDIR /app

# คัดลอกไฟล์ requirements.txt ไปยัง Working directory
COPY requirements.txt .

# ติดตั้ง Python packages ที่ระบุใน requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์โค้ดของ API ทั้งหมดไปยัง Working directory
COPY app.py .

# กำหนดพอร์ตที่ Container จะเปิด (ตรงกับ app.run() ใน app.py)
EXPOSE 8001

# คำสั่งสำหรับรัน Flask app เมื่อ Container เริ่มต้น
CMD ["python", "app.py"]
5. ไฟล์ docker-compose.yml
ไฟล์นี้จะกำหนดและรัน Docker Container ของทั้งสอง API ของเรา:

YAML

version: '3.8'

services:
  api1:
    build: ./api1 # Path ไปยังโฟลเดอร์ของ API 1 ที่มี Dockerfile
    container_name: api1_container
    ports:
      - "8000:8000" # แมปพอร์ต 8000 ของ Host ไปยังพอร์ต 8000 ของ Container API 1
    environment:
      # URL ของ API 2 ที่ API 1 จะเรียกใช้
      # ใช้ชื่อ service ใน Docker Compose ("api2") เพื่อให้ Docker จัดการ DNS resolution ให้
      API2_URL: http://api2:8001/api2-hello
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  api2:
    build: ./api2 # Path ไปยังโฟลเดอร์ของ API 2 ที่มี Dockerfile
    container_name: api2_container
    ports:
      - "8001:8001" # แมปพอร์ต 8001 ของ Host ไปยังพอร์ต 8001 ของ Container API 2
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
6. ไฟล์ README.md
ไฟล์นี้จะบอกวิธีการ Deploy และทดสอบโปรเจกต์อย่างละเอียด:

Markdown

# API Chaining with Docker Compose (2 Containers - Hello World)

โปรเจกต์นี้สาธิตการทำงานของ API สองตัวที่แยกกันอยู่คนละ Docker Container (API 1 และ API 2) และมีการเชื่อมโยงการทำงานระหว่างกัน: API 1 จะส่ง Request ไปยัง API 2 และนำคำตอบจาก API 2 กลับมาแสดงผลให้ผู้ใช้.

---

## คุณสมบัติ

* **API 1 (Gateway):** รับ GET Request ที่ `/api1-hello` จากผู้ใช้, พิมพ์ Log, ส่งต่อ Request ไปยัง API 2, พิมพ์ Log, รับคำตอบจาก API 2, พิมพ์ Log, และส่งคำตอบรวมกลับคืนให้ผู้ใช้
* **API 2 (Processor):** รับ GET Request ที่ `/api2-hello` จาก API 1, พิมพ์ Log, สร้างคำตอบ "Hello from API 2!", พิมพ์ Log, และส่งคำตอบกลับไปให้ API 1
* **ภาษาที่ใช้:** Python (Flask Framework)
* **การจัดการ Container:** Docker และ Docker Compose (ทำให้มี 2 Containers แยกกัน)
* **การบันทึก Log:** มีการ Print logs ทั้งบน API1 และ API2 เพื่อให้เห็น Workflow การทำงาน

---

## ความต้องการเบื้องต้น (Prerequisites)

* [**Docker Desktop**](https://www.docker.com/products/docker-desktop/) (รวม Docker Engine และ Docker Compose) ติดตั้งบนเครื่องของคุณ

---

## โครงสร้างโปรเจกต์

.
├── api1/                 # โฟลเดอร์สำหรับ API 1
│   ├── app.py            # โค้ด Python ของ API 1
│   ├── requirements.txt  # รายการ Package Python ที่จำเป็นสำหรับ API 1
│   └── Dockerfile        # คำสั่งสำหรับสร้าง Docker Image ของ API 1
├── api2/                 # โฟลเดอร์สำหรับ API 2
│   ├── app.py            # โค้ด Python ของ API 2
│   ├── requirements.txt  # รายการ Package Python ที่จำเป็นสำหรับ API 2
│   └── Dockerfile        # คำสั่งสำหรับสร้าง Docker Image ของ API 2
├── docker-compose.yml    # ไฟล์สำหรับกำหนดและจัดการ Docker services (2 Services = 2 Containers)
└── README.md             # ไฟล์นี้


---

## วิธีการ Deploy และรัน

1.  **Clone Repository:**
    ```bash
    git clone <URL_ของ_GitHub/GitLab_Repository_ของคุณ>
    cd <ชื่อโฟลเดอร์ Repository ของคุณ>
    ```
    (หรือสร้างโครงสร้างโฟลเดอร์และไฟล์ด้วยตัวเอง)

2.  **สร้างและรัน Docker Containers:**
    จากไดเรกทอรีรูทของโปรเจกต์ (ที่ไฟล์ `docker-compose.yml` อยู่) รันคำสั่งนี้:
    ```bash
    docker-compose up -d --build
    ```
    * `docker-compose up`: สร้างและรัน Services ที่กำหนดใน `docker-compose.yml`
    * `-d`: รัน Container ในโหมด Detached (ทำงานเบื้องหลัง)
    * `--build`: บังคับให้ Docker สร้าง Image ใหม่จาก Dockerfile ทุกครั้ง (สำคัญเมื่อมีการเปลี่ยนแปลงโค้ด)

    รอจนกระทั่งกระบวนการเสร็จสมบูรณ์ Docker จะทำการดาวน์โหลด Python base image, ติดตั้ง dependencies, และรัน API ทั้งสอง.

---

## วิธีการทดสอบ

เมื่อ Containers รันอยู่ คุณสามารถทดสอบ API ได้ดังนี้:

1.  **ทดสอบ API 1 (Gateway) - Endpoint ที่มีการเรียก API 2:**
    เปิด Terminal หรือ Command Prompt อันใหม่แล้วใช้ `curl` หรือเปิด Web Browser:

    * **ผ่าน `curl`:**
        ```bash
        curl http://localhost:8000/api1-hello
        ```
        คุณควรจะได้รับ JSON Response ที่รวมข้อความจาก API 2:
        ```json
        {
          "message_from_api1": "Hello from API 1! (Request forwarded to API 2)",
          "message_from_api2": "Hello from API 2!"
        }
        ```

    * **ผ่าน Web Browser:**
        เปิด `http://localhost:8000/api1-hello` ในเบราว์เซอร์ของคุณ คุณจะเห็น JSON Response คล้ายกับด้านบน

---

## การดู Logs

คุณสามารถดู Log ของแต่ละ API เพื่อตรวจสอบการทำงานและลำดับการเรียก:

* **ดู Log ของ API 1:**
    ```bash
    docker-compose logs api1
    ```
    คุณควรจะเห็น Log ที่บอกว่า `API1 LOG: Received GET request from user...`, `API1 LOG: Forwarding request to API 2...`, และ `API1 LOG: Received response from API 2...`

* **ดู Log ของ API 2:**
    ```bash
    docker-compose logs api2
    ```
    คุณควรจะเห็น Log ที่บอกว่า `API2 LOG: Received GET request from API 1...` และ `API2 LOG: Sending response back to API 1...`

* **ดู Log ของทั้งสอง API พร้อมกัน:**
    ```bash
    docker-compose logs
    ```

---

## การหยุดและลบ Containers

เมื่อคุณทดสอบเสร็จแล้ว คุณสามารถหยุดและลบ Containers ได้ด้วยคำสั่ง:

```bash
docker-compose down

ถ้าต้องการลบ 
docker-compose down --rmi all