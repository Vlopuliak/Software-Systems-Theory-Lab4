from fastapi import FastAPI, HTTPException
import os

STUDENT_N = int(os.getenv("STUDENT_N", 9))
app = FastAPI(title=f"Employee Service N{STUDENT_N}")

# База даних працівників (ID починаються з 100 * 9 + 1) [cite: 345-347, 407]
EMPLOYEES = {
    901: {"id": 901, "name": "Вадим", "position": "Lead Gen Manager"},
    902: {"id": 902, "name": "Олексій", "position": "Developer"}
}

@app.get("/employees/{emp_id}")
def get_employee(emp_id: int):
    if emp_id not in EMPLOYEES:
        raise HTTPException(status_code=404, detail="Employee not found")
    # Обов'язкове поле student_id для звіту [cite: 408]
    return {"student_id": STUDENT_N, "data": EMPLOYEES[emp_id]}