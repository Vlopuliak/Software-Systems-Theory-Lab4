from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

STUDENT_N = int(os.getenv("STUDENT_N", 9))
app = FastAPI(title=f"Attendance Service N{STUDENT_N}")
# Використовуємо ім'я сервісу з docker-compose [cite: 302]
EMPLOYEE_SERVICE_URL = "http://employee-service:8000"


class AttendanceLog(BaseModel):
    emp_id: int
    hours: int


@app.post("/log-time")
def log_time(log: AttendanceLog):
    try:
        # Синхронний запит до сервісу працівників [cite: 311-313]
        resp = requests.get(f"{EMPLOYEE_SERVICE_URL}/employees/{log.emp_id}")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Employee Service is unavailable")

    if resp.status_code == 404:
        raise HTTPException(status_code=400, detail="Employee does not exist")

    emp_name = resp.json()["data"]["name"]
    return {
        "student_id": STUDENT_N,
        "message": f"Recorded {log.hours} hours for {emp_name}",
        "status": "Success"
    }