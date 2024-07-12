from fastapi import APIRouter, Depends, HTTPException
from typing import List
import models
import auth
from datetime import datetime
from database import users_collection, appointments_collection

router = APIRouter()


# Get all users
@router.get("/users")
async def read_all_users(
    current_user: models.User = Depends(auth.get_current_active_admin),
):
    users = await users_collection.find().to_list(None)
    return [models.User(**user) for user in users]


# Admin delete user
@router.delete("/users/{phone}", response_model=models.User)
async def delete_user(
    phone: str, current_user: models.UserInDB = Depends(auth.get_current_active_admin)
):
    user = await users_collection.find_one({"phone": phone})
    if user:
        await appointments_collection.delete_many({"phone": phone})
        await users_collection.delete_one({"phone": phone})
        return models.UserInDB(**user)
    raise HTTPException(status_code=404, detail="User not found")


# Get all appointments for a phone number
@router.get("/appointments/phone/{phone}", response_model=List[models.Appointment])
async def get_appointments_by_phone(
    phone: str, current_user: models.UserInDB = Depends(auth.get_current_active_admin)
):
    appointments = await appointments_collection.find({"phone": phone}).to_list(None)
    if not appointments:
        raise HTTPException(
            status_code=404, detail="Appointments not found for this phone number"
        )
    sorted_appointments = sorted(
        appointments,
        key=lambda x: (
            datetime.strptime(x["date"], "%d-%m-%Y"),
            datetime.strptime(x["time"], "%H:%M"),
        ),
    )
    return sorted_appointments


# Get all appointments in a specific month and year
@router.get(
    "/appointments/month/{month}/year/{year}", response_model=List[models.Appointment]
)
async def get_appointments_by_month_and_year(
    month: int,
    year: int,
    current_user: models.UserInDB = Depends(auth.get_current_active_admin),
):
    appointments = await appointments_collection.find().to_list(None)
    appointments_list = []
    for a in appointments:
        appointment_datetime = models.combine_date_time(a["date"], a["time"])
        if appointment_datetime.month == month and appointment_datetime.year == year:
            appointments_list.append(a)
    if not appointments_list:
        raise HTTPException(
            status_code=404, detail="Appointments not found for this month and year"
        )
    sorted_appointments = sorted(
        appointments_list,
        key=lambda x: (
            datetime.strptime(x["date"], "%d-%m-%Y"),
            datetime.strptime(x["time"], "%H:%M"),
        ),
    )
    return sorted_appointments
