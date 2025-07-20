# API Chaining with Docker Compose (2 Interactive Containers)

โปรเจกต์นี้สาธิตการทำงานของ API สองตัวที่แยกกันอยู่คนละ Docker Container (API 1 และ API 2) และมีการเชื่อมโยงการทำงานระหว่างกันโดย User request ไปที่ API 1 และ API 1 ส่ง Request ต่อไปยัง API 2 และนำคำตอบจาก API 2 กลับมาแสดงผลให้ User.

# Getting Started

1. Clone Repository
เปิด Terminal หรือ Command Prompt ของคุณ แล้วโคลนโปรเจกต์นี้ลงบนเครื่อง
         
       git clone https://github.com/kritsapdev/ai-for-thai-api-quiz.git

2.     cd ai-for-thai-api-quiz

3. Deploy and Run Containers (ติดตั้งและรัน Docker Containers)
จากไดเรกทอรีหลักของโปรเจกต์ (ที่ไฟล์ docker-compose.yml อยู่) รันคำสั่งนี้
         
       docker-compose up -d --build

4. Test the API (ทดสอบ API) ทดสอบผ่าน curl (ใน Terminal) โดยเปิด Terminal แล้วรันคำสั่ง
 
       curl -X POST -H "Content-Type: application/json" -d "{\"text\": \"This data to API Chain\"}" http://localhost:8000/api1-process

   ผลลัพธ์จะได้ดังนี้
   
       {"message_from_api1":"API 1 processed your request and got a response from API 2.","original_text_sent_by_user":"This data to API Chain","response_from_api2":{"api_name":"API 2 Responder","message":"API 2 received your message: 'This data to API Chain'","processed_at_api2":"2025-07-20 12:38:59","your_input_was":"This data to API Chain"}, "status":"success"}

      สามารถร run ผ่าน postman ได้ด้วย url 

       http://localhost:8000/api1-process 

5. การดู Logs

คุณสามารถดู Log ของแต่ละ API เพื่อตรวจสอบการทำงานและลำดับการเรียก ด้วยคำสั่ง

    docker-compose logs api1
สำหรับดู  logs api1  และ

    docker-compose logs api2
สำหรับดู  logs api2

หรือดู log พร้อมกันทั้ง api1 , api2  
  
    docker-compose logs

6. การหยุดและลบ Docker
คุณสามารถหยุดและลบ Docker Containers ที่สร้างขึ้นมาได้ด้วยคำสั่ง

    docker-compose down


หากต้องการลบ Docker Images ที่สร้างขึ้นมาด้วย


    docker-compose down --rmi all   





