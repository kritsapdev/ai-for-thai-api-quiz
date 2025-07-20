# API Chaining with Docker Compose (2 Interactive Containers)

โปรเจกต์นี้สาธิตการทำงานของ API สองตัวที่แยกกันอยู่คนละ Docker Container (API 1 และ API 2) และมีการเชื่อมโยงการทำงานระหว่างกันโดย User request ไปที่ API 1 และ API 1 ส่ง Request ต่อไปยัง API 2 และนำคำตอบจาก API 2 กลับมาแสดงผลให้ User.

---

# Getting Started

1. Clone Repository
เปิด Terminal หรือ Command Prompt ของคุณ แล้วโคลนโปรเจกต์นี้ลงบนเครื่อง
git clone xxx
cd xxx
---

2. Deploy and Run Containers (ติดตั้งและรัน Docker Containers)
จากไดเรกทอรีหลักของโปรเจกต์ (ที่ไฟล์ docker-compose.yml อยู่) รันคำสั่งนี้
docker-compose up -d --build
---

3. Test the API (ทดสอบ API)
3.1 ทดสอบผ่าน curl (ใน Terminal)
   เปิด Terminal แล้วรันคำสั่ง 
   curl -X POST -H "Content-Type: application/json" -d "{\"text\": \"นี่คือข้อความที่ฉันต้องการส่งผ่าน API Chain\"}" http://localhost:8000/api1-process

   ผลลัพธ์จะได้ดังนี้
   {
    "message_from_api1":"API 1 processed your request and got a response from API 2.",
    "original_text_sent_by_user":"นี่คือข้อความที่ฉันต้องการส่งผ่าน API Chain",
    "response_from_api2":
        {
            "api_name":"API 2 Responder",
            "message":"API 2 received your message: 'นี่คือข้อความที่ฉันต้องการส่งผ่าน API Chain'",
            "processed_at_api2":"2025-07-20 12:38:59",
            "your_input_was":"นี่คือข้อความที่ฉันต้องการส่งผ่าน API Chain"
        },
        "status":"success"
    }

3.2 ผ่าน Postman
    Method เป็น POST
    URL เป็น http://localhost:8000/api1-process
    ที่แท็บ Headers 
        Key: Content-Type
        Value: application/json
---

4. การดู Logs
คุณสามารถดู Log ของแต่ละ API เพื่อตรวจสอบการทำงานและลำดับการเรียก ด้วยคำสั่ง
    docker-compose logs api1
    docker-compose logs api2
หรือดู log พร้อมกันทั้ง api1 , api2    
    docker-compose logs
---

5. การหยุดและลบ Docker
คุณสามารถหยุดและลบ Docker Containers ที่สร้างขึ้นมาได้ด้วยคำสั่ง
docker-compose down

หากต้องการลบ Docker Images ที่สร้างขึ้นมาด้วย
docker-compose down --rmi all

