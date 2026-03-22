from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# Data
doctors = [
    {"id": 1, "name": "Dr. Rajesh Kumar", "specialization": "Cardiologist", "fee": 800, "experience_years": 12, "is_available": True},
    {"id": 2, "name": "Dr. Priya Sharma", "specialization": "Dermatologist", "fee": 500, "experience_years": 8, "is_available": True},
    {"id": 3, "name": "Dr. Arjun Mehta", "specialization": "Pediatrician", "fee": 600, "experience_years": 10, "is_available": False},
    {"id": 4, "name": "Dr. Neha Singh", "specialization": "General", "fee": 300, "experience_years": 5, "is_available": True},
    {"id": 5, "name": "Dr. Vikram Patel", "specialization": "Cardiologist", "fee": 900, "experience_years": 15, "is_available": False},
    {"id": 6, "name": "Dr. Anjali Verma", "specialization": "Dermatologist", "fee": 450, "experience_years": 7, "is_available": True},
]

appointments = []
appt_counter = 1
doctor_counter = 7


# Task6
class AppointmentRequest(BaseModel):
    patient_name: str = Field(..., min_length=2)
    doctor_id: int = Field(..., gt=0)
    date: str = Field(..., min_length=8)
    reason: str = Field(..., min_length=5)
    appointment_type: str = "in-person"
    senior_citizen: bool = False


# Task11
class NewDoctor(BaseModel):
    name: str = Field(..., min_length=2)
    specialization: str = Field(..., min_length=2)
    fee: int = Field(..., gt=0)
    experience_years: int = Field(..., gt=0)
    is_available: bool = True


# Helpers
def find_doctor(doctor_id: int):
    for d in doctors:
        if d["id"] == doctor_id:
            return d
    return None


def find_appointment(appt_id: int):
    for a in appointments:
        if a["appointment_id"] == appt_id:
            return a
    return None


def calculate_fee(base_fee, appointment_type, senior):
    if appointment_type == "video":
        fee = base_fee * 0.8
    elif appointment_type == "emergency":
        fee = base_fee * 1.5
    else:
        fee = base_fee

    original = int(fee)

    if senior:
        fee *= 0.85

    return original, int(fee)


def filter_doctors_logic(specialization, max_fee, min_experience, is_available):
    result = doctors

    if specialization is not None:
        result = [d for d in result if d["specialization"] == specialization]

    if max_fee is not None:
        result = [d for d in result if d["fee"] <= max_fee]

    if min_experience is not None:
        result = [d for d in result if d["experience_years"] >= min_experience]

    if is_available is not None:
        result = [d for d in result if d["is_available"] == is_available]

    return result


# Task1
@app.get("/")
def root():
    return {"message": "Welcome to MediCare Clinic"}


# Task2
@app.get("/doctors")
def get_doctors():
    return {
        "doctors": doctors,
        "total": len(doctors),
        "available_count": sum(1 for d in doctors if d["is_available"])
    }


# Task5
@app.get("/doctors/summary")
def doctors_summary():
    return {
        "total_doctors": len(doctors),
        "available_doctors": sum(1 for d in doctors if d["is_available"]),
        "most_experienced_doctor": max(doctors, key=lambda d: d["experience_years"])["name"],
        "cheapest_fee": min(d["fee"] for d in doctors),
        "specialization_count": {
            s: len([d for d in doctors if d["specialization"] == s])
            for s in set(d["specialization"] for d in doctors)
        }
    }


# Task10
@app.get("/doctors/filter")
def filter_doctors(specialization: str = None, max_fee: int = None,
                   min_experience: int = None, is_available: bool = None):
    result = filter_doctors_logic(specialization, max_fee, min_experience, is_available)
    return {"doctors": result, "count": len(result)}



# Task16: Search doctors by keyword
@app.get("/doctors/search")
def search_doctors(keyword: str):
    result = [
        d for d in doctors
        if keyword.lower() in d["name"].lower()
        or keyword.lower() in d["specialization"].lower()
    ]

    if not result:
        return {"message": "No doctors found", "total_found": 0}

    return {"doctors": result, "total_found": len(result)}


# Task17: Sort doctors
@app.get("/doctors/sort")
def sort_doctors(sort_by: str = "fee"):
    valid_fields = ["fee", "name", "experience_years"]

    if sort_by not in valid_fields:
        raise HTTPException(400, "Invalid sort field")

    sorted_list = sorted(doctors, key=lambda d: d[sort_by])

    return {
        "sort_by": sort_by,
        "order": "asc",
        "doctors": sorted_list
    }
    
    
import math

# Task18: Paginate doctors
@app.get("/doctors/page")
def paginate_doctors(page: int = 1, limit: int = 3):
    total = len(doctors)
    total_pages = math.ceil(total / limit)

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "doctors": doctors[start:end]
    }
    
    
# Task19: Search appointments
@app.get("/appointments/search")
def search_appointments(patient_name: str):
    result = [
        a for a in appointments
        if patient_name.lower() in a["patient"].lower()
    ]
    return {"appointments": result, "count": len(result)}


# Task19: Sort appointments
@app.get("/appointments/sort")
def sort_appointments(sort_by: str = "fee"):
    if sort_by == "fee":
        key_func = lambda a: a["final_fee"]
    elif sort_by == "date":
        key_func = lambda a: a["date"]
    else:
        raise HTTPException(400, "Invalid sort field")

    return {"appointments": sorted(appointments, key=key_func)}


# Task19: Paginate appointments
@app.get("/appointments/page")
def paginate_appointments(page: int = 1, limit: int = 3):
    total = len(appointments)
    total_pages = math.ceil(total / limit)

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "appointments": appointments[start:end]
    }
    
    
# Task20: Browse doctors (filter + sort + paginate)
@app.get("/doctors/browse")
def browse_doctors(
    keyword: str = None,
    sort_by: str = "fee",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = doctors

    # Filter
    if keyword:
        result = [
            d for d in result
            if keyword.lower() in d["name"].lower()
            or keyword.lower() in d["specialization"].lower()
        ]

    # Sort
    valid_fields = ["fee", "name", "experience_years"]
    if sort_by not in valid_fields:
        raise HTTPException(400, "Invalid sort field")

    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda d: d[sort_by], reverse=reverse)

    # Pagination
    total = len(result)
    total_pages = math.ceil(total / limit)

    start = (page - 1) * limit
    end = start + limit

    return {
        "total": total,
        "total_pages": total_pages,
        "page": page,
        "limit": limit,
        "sort_by": sort_by,
        "order": order,
        "results": result[start:end]
    }
    


# Task3
@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    doctor = find_doctor(doctor_id)
    if not doctor:
        raise HTTPException(404, "Doctor not found")
    return doctor


# Task11: Create doctor
@app.post("/doctors", status_code=201)
def create_doctor(new_doc: NewDoctor):
    global doctor_counter

    for d in doctors:
        if d["name"].lower() == new_doc.name.lower():
            raise HTTPException(400, "Doctor with this name already exists")

    doctor = {"id": doctor_counter, **new_doc.dict()}
    doctors.append(doctor)
    doctor_counter += 1
    return doctor


# Task12: Update doctor
@app.put("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, fee: int = None, is_available: bool = None):
    doctor = find_doctor(doctor_id)
    if not doctor:
        raise HTTPException(404, "Doctor not found")

    if fee is not None:
        doctor["fee"] = fee
    if is_available is not None:
        doctor["is_available"] = is_available

    return doctor


# Task13: Delete doctor
@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    doctor = find_doctor(doctor_id)
    if not doctor:
        raise HTTPException(404, "Doctor not found")

    for a in appointments:
        if a["doctor"] == doctor["name"] and a["status"] == "scheduled":
            raise HTTPException(400, "Doctor has active appointments")

    doctors.remove(doctor)
    return {"message": "Doctor deleted"}


# Task4
@app.get("/appointments")
def get_appointments():
    return {"appointments": appointments, "total": len(appointments)}


# Task8 + Task9
@app.post("/appointments")
def create_appointment(req: AppointmentRequest):
    global appt_counter

    doctor = find_doctor(req.doctor_id)
    if not doctor:
        raise HTTPException(404, "Doctor not found")
    if not doctor["is_available"]:
        raise HTTPException(400, "Doctor not available")

    original, final = calculate_fee(doctor["fee"], req.appointment_type, req.senior_citizen)

    appointment = {
        "appointment_id": appt_counter,
        "patient": req.patient_name,
        "doctor": doctor["name"],
        "doctor_id": doctor["id"],
        "date": req.date,
        "type": req.appointment_type,
        "original_fee": original,
        "final_fee": final,
        "status": "scheduled"
    }

    appointments.append(appointment)
    appt_counter += 1
    return appointment


# Task14: Confirm appointment (also mark doctor unavailable)
@app.post("/appointments/{appointment_id}/confirm")
def confirm_appt(appointment_id: int):
    appt = find_appointment(appointment_id)
    if not appt:
        raise HTTPException(404, "Appointment not found")

    appt["status"] = "confirmed"

    doctor = find_doctor(appt["doctor_id"])
    if doctor:
        doctor["is_available"] = False

    return appt


# Task14: Cancel appointment
@app.post("/appointments/{appointment_id}/cancel")
def cancel_appt(appointment_id: int):
    appt = find_appointment(appointment_id)
    if not appt:
        raise HTTPException(404, "Appointment not found")

    appt["status"] = "cancelled"

    doctor = find_doctor(appt["doctor_id"])
    if doctor:
        doctor["is_available"] = True

    return appt


# Task15: Complete appointment
@app.post("/appointments/{appointment_id}/complete")
def complete_appt(appointment_id: int):
    appt = find_appointment(appointment_id)
    if not appt:
        raise HTTPException(404, "Appointment not found")

    appt["status"] = "completed"
    return appt


# Task15: Active appointments (IMPORTANT: above variable route)
@app.get("/appointments/active")
def active_appointments():
    result = [a for a in appointments if a["status"] in ["scheduled", "confirmed"]]
    return {"appointments": result, "count": len(result)}


# Task15: Appointments by doctor
@app.get("/appointments/by-doctor/{doctor_id}")
def appointments_by_doctor(doctor_id: int):
    result = [a for a in appointments if a["doctor_id"] == doctor_id]
    return {"appointments": result, "count": len(result)}