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