from fastapi import APIRouter, Depends, HTTPException
from typing import List
import models
import auth
from database import appointments_collection
from datetime import datetime

router = APIRouter()


# Function to calculate the correct id for appointments
async def get_next_id():
    last_appointment = (
        await appointments_collection.find().sort("id", -1).limit(1).to_list(1)
    )
    if last_appointment:
        return last_appointment[0]["id"] + 1
    else:
        return 1


# Create an appointment
@router.post("/appointments", response_model=models.Appointment)
async def create_appointment(
    appointment: models.Appointment,
    current_user: models.UserInDB = Depends(auth.get_current_active_user),
):
    try:
        appointment.id = await get_next_id()
        appointment_dict = appointment.model_dump()
        appointment_dict["phone"] = str(current_user.phone)
        await appointments_collection.insert_one(appointment_dict)
        return models.Appointment(**appointment_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all appointments for all users
@router.get("/appointments/all", response_model=List[models.Appointment])
async def get_all_appointments(
    current_user: models.UserInDB = Depends(auth.get_current_active_user),
):
    appointments = await appointments_collection.find().to_list(None)
    if not appointments:
        raise HTTPException(status_code=404, detail="Appointments not found")
    sorted_appointments = sorted(
        appointments,
        key=lambda x: (
            datetime.strptime(x["date"], "%d-%m-%Y"),
            datetime.strptime(x["time"], "%H:%M"),
        ),
    )
    return sorted_appointments


# Get all appointments for a specific user
@router.get("/appointments", response_model=List[models.Appointment])
async def get_appointments(
    current_user: models.UserInDB = Depends(auth.get_current_active_user),
):
    appointments = await appointments_collection.find(
        {"phone": current_user.phone}
    ).to_list(None)
    if not appointments:
        raise HTTPException(status_code=404, detail="Appointments not found")
    sorted_appointments = sorted(
        appointments,
        key=lambda x: (
            datetime.strptime(x["date"], "%d-%m-%Y"),
            datetime.strptime(x["time"], "%H:%M"),
        ),
    )
    return sorted_appointments


# Update appointment by id
@router.put("/appointments/{id}", response_model=models.Appointment)
async def update_appointment(
    id: int,
    updated_appointment: models.Appointment,
    current_user: models.UserInDB = Depends(auth.get_current_active_user),
):
    existing_appointment = await appointments_collection.find_one({"id": id})
    if existing_appointment:
        if (
            existing_appointment["phone"] == current_user.phone
            or current_user.role == "admin"
        ):
            updated_appointment_dict = updated_appointment.model_dump()
            await appointments_collection.update_one(
                {"id": id}, {"$set": updated_appointment_dict}
            )
            return updated_appointment
        else:
            raise HTTPException(
                status_code=403, detail="Not authorized to update this appointment"
            )
    raise HTTPException(status_code=404, detail="Can't update, appointment not found")


# Delete appointment by id
@router.delete("/appointments/{id}", response_model=models.Appointment)
async def delete_appointment(
    id: int, current_user: models.UserInDB = Depends(auth.get_current_active_user)
):
    existing_appointment = await appointments_collection.find_one({"id": id})
    if existing_appointment:
        if (
            existing_appointment["phone"] == current_user.phone
            or current_user.role == "admin"
        ):
            await appointments_collection.delete_one({"id": id})
            return existing_appointment
        else:
            raise HTTPException(
                status_code=403, detail="Not authorized to delete this appointment"
            )
    raise HTTPException(status_code=404, detail="Appointment not found")
