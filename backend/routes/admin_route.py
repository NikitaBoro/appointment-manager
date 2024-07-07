from fastapi import APIRouter, Depends, HTTPException
from typing import List
import models
import auth
from data import appointments, db
from datetime import datetime

router = APIRouter()


# Get all users
@router.get("/users")
def read_all_users(current_user: models.User = Depends(auth.get_current_active_admin)):
    return [models.User(**user_data) for user_data in db.values()]


# Admin delete user
@router.delete("/users/{phone}", response_model=models.User)
def delete_user(
    phone: str, current_user: models.UserInDB = Depends(auth.get_current_active_admin)
):
    if phone in db:
        updated_appointments = []
        for appointment in appointments:
            if appointment["phone"] != phone:
                updated_appointments.append(appointment)

        appointments[:] = updated_appointments
        user = db.pop(phone)
        return models.UserInDB(**user)
    raise HTTPException(status_code=404, detail="User not found")


# Get all appointments for a phone number
@router.get("/appointments/phone/{phone}", response_model=List[models.Appointment])
def get_appointments_by_phone(
    phone: str, current_user: models.UserInDB = Depends(auth.get_current_active_admin)
):
    appointments_list = []
    for a in appointments:
        if a["phone"] == phone:
            appointments_list.append(a)
    if not appointments_list:
        raise HTTPException(
            status_code=404, detail="Appointments not found for this phone number"
        )
    appointments_list.sort(key=lambda x: (datetime.strptime(x['date'], "%d-%m-%Y"), datetime.strptime(x['time'], "%H:%M")))
    return appointments_list


# Get all appointments in a specific month and year
@router.get("/appointments/month/{month}/year/{year}", response_model=List[models.Appointment])
def get_appointments_by_month_and_year(
    month: int, year: int, current_user: models.UserInDB = Depends(auth.get_current_active_admin)
):
    appointments_list = []
    for a in appointments:
        appointment_datetime = models.combine_date_time(a["date"], a["time"])
        if appointment_datetime.month == month and appointment_datetime.year == year:
            appointments_list.append(a)

    if not appointments_list:
        raise HTTPException(
            status_code=404, detail="Appointments not found for this month and year"
        )
        
    appointments_list.sort(key=lambda x: (datetime.strptime(x['date'], "%d-%m-%Y"), datetime.strptime(x['time'], "%H:%M")))
    return appointments_list
