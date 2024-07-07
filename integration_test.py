import pytest
import sys
from fastapi.testclient import TestClient

sys.path.append('./backend')

from backend.main import app
from backend.data import appointments,current_id,db
import backend.auth as auth


client = TestClient(app)


# Helper functions---------------------------------------------------------------------------------------


# Helper function to register a user
def register_user(phone: str = "1234567890", full_name: str="Test User", email: str="test@example.com", password: str = "password123", role: str = "user"):
    response = client.post("/v1/register", json={
        "phone": phone,
        "full_name": full_name,
        "email": email,
        "role": role
    }, params={"password": password})
    return response

# Helper function to login and get token
def login_user(phone: str, password: str):
    response = client.post("/v1/token", data={"username": phone, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# Helper function to create an appointment
def create_appointment(token_headers: dict, appointment_data: dict = {
        "id": current_id,
        "name": "Test User",
        "phone": "1234567890",
        "date": "17-10-2024",
        "time": "10:00",
        "service": "Manicure"
    }):
    response = client.post("/v1/appointments", json=appointment_data, headers=token_headers)
    return response


# Tests -----------------------------------------------------------------------------------------------------


def test_user_workflow():
    # Register user
    response = register_user()
    assert response.status_code == 200

    # Login user
    headers = login_user("1234567890", "password123")

    # Create first appointment
    first_appointment = create_appointment(headers)
    assert first_appointment.status_code == 200
    
    # Create second appointment
    second_appointment = create_appointment(
        headers,
        {
            "id": current_id+1,
            "name": "Test User",
            "phone": "1234567890",
            "date": "20-10-2024",
            "time": "13:00","service": "Manicure",
        },
    )
    assert second_appointment.status_code == 200
    
    # Get all appointments
    response = client.get("/v1/appointments", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    print("Appointments: ",data)
    assert data[0]["id"] == 1
    assert data[0]["phone"] == "1234567890"
    assert data[0]["name"] == "Test User"
    assert data[0]["date"] == "17-10-2024"
    assert data[0]["time"] == "10:00"
    assert data[0]["service"] == "Manicure"
    
    assert data[1]["id"] == 2
    assert data[1]["phone"] == "1234567890"
    assert data[1]["name"] == "Test User"
    assert data[1]["date"] == "20-10-2024"
    assert data[1]["time"] == "13:00"
    assert data[1]["service"] == "Manicure"
    
    # Update first appointment
    update_response = client.put(
        f"/v1/appointments/{data[0]["id"]}",
        json={
            "id": data[0]["id"],
            "name": "Test User",
            "phone": "1234567890",
            "date": "18-10-2024",
            "time": "16:00",
            "service": "Pedicure",
        },
        headers=headers,
    )
    assert update_response.status_code == 200
    data_updated_appointment = update_response.json()
    print("Update Appointments: ",data_updated_appointment)
    assert data_updated_appointment["id"] == 1
    assert data_updated_appointment["name"] == "Test User"
    assert data_updated_appointment["date"] == "18-10-2024"
    assert data_updated_appointment["time"] == "16:00"
    assert data_updated_appointment["service"] == "Pedicure"
    
    # Delete second appointment
    delete_response = client.delete(
        f"/v1/appointments/{data[1]["id"]}", headers=headers
    )
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["id"] == data[1]["id"]

    # Verify the appointment is deleted:
    get_response = client.get("/v1/appointments", headers=headers)
    assert get_response.status_code == 200
    data_after_deletion = get_response.json()
    print("after deletion: ",data_after_deletion)
    assert not any(app["id"] == data[1]["id"] for app in data_after_deletion)



def test_admin_workflow():
    # Register users
    register_user(phone="1111111111", full_name="Test User", email="test@example.com", password="password123", role="user")
    register_user(phone="2222222222", full_name="Test User2", email="test2@example.com", password="password123", role="user")

    # Login as admin
    admin_headers = login_user("admin", "admin")

    # Get all users
    response = client.get("/v1/admin/users", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4

    # Delete a user
    delete_response = client.delete("/v1/admin/users/1111111111", headers=admin_headers)
    assert delete_response.status_code == 200

    # Verify user deletion
    get_users_response = client.get("/v1/admin/users", headers=admin_headers)
    assert get_users_response.status_code == 200
    users_data = get_users_response.json()
    assert not any(user["phone"] == "1111111111" for user in users_data)

    # Create appointments for testing
    user_headers = login_user("2222222222", "password123")
    create_appointment(user_headers, {
        "id": current_id + 1,
        "name": "Test User2",
        "phone": "2222222222",
        "date": "17-10-2024",
        "time": "10:00",
        "service": "Manicure"
    })
    create_appointment(user_headers, {
        "id": current_id + 1,
        "name": "Test User2",
        "phone": "2222222222",
        "date": "18-10-2024",
        "time": "11:00",
        "service": "Pedicure"
    })
    
    # Get all appointments as admin
    get_appointments_response = client.get("/v1/appointments/all", headers=admin_headers)
    assert get_appointments_response.status_code == 200
    appointments_data = get_appointments_response.json()
    print("data: ",appointments_data)
    assert len(appointments_data) == 3
    assert appointments_data[0]["id"] == 3
    assert appointments_data[1]["id"] == 4
    assert appointments_data[2]["id"] == 1
    
    # Get appointments by phone
    response = client.get(
        "/v1/admin/appointments/phone/2222222222", headers=admin_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["phone"] == "2222222222"
    
    #Get appointments by month and year
    response = client.get("/v1/admin/appointments/month/10/year/2024", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["date"].split("-")[1] == "10"
    assert data[1]["date"].split("-")[1] == "10"
    assert data[2]["date"].split("-")[1] == "10"
    
