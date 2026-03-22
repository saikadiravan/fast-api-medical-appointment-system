# 🏥 Medical Appointment Management System (FastAPI)

This project is a backend system built using FastAPI as part of my internship training.  
It simulates a real-world medical appointment system where users can manage doctors, schedule appointments, and perform various operations like filtering, searching, and tracking appointment workflows.

---

## 🚀 What I Built

I designed and implemented a complete REST API system that allows:

- Managing doctors (add, update, delete)
- Booking appointments
- Handling appointment workflows (confirm, cancel, complete)
- Applying dynamic pricing logic
- Searching, filtering, sorting, and paginating data

The goal was to build a realistic backend system with proper structure and logic.

---

## ⚙️ Tech Stack

- **FastAPI**
- **Python**
- **Pydantic (for validation)**
- **Uvicorn (server)**

---

## ✨ Key Features

### 👨‍⚕️ Doctor Management
- Add new doctors
- Update doctor details (fee, availability)
- Delete doctors with validation (cannot delete if active appointments exist)
- Filter doctors by specialization, fee, experience, and availability
- Search doctors by name or specialization
- Sort doctors by fee, name, or experience
- Pagination support

---

### 📅 Appointment Management
- Book appointments with validation
- Dynamic fee calculation:
  - Video → 80% of fee  
  - Emergency → 150% of fee  
  - Senior citizen → extra 15% discount  
- Appointment lifecycle:
  - Scheduled → Confirmed → Completed / Cancelled
- Automatically updates doctor availability

---

### 🔍 Advanced Features
- Search appointments by patient name
- Sort appointments by fee or date
- Paginate appointments
- Combined Browse API (filter + sort + paginate)

---

## 📌 API Highlights

- RESTful API design
- Input validation using Pydantic
- Error handling using HTTPException
- Modular helper functions
- Real-world business logic implementation

---

## 🧪 API Testing

All endpoints were tested using Swagger UI.

To run locally:

```bash
uvicorn main:app --reload
