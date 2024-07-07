import requests
import streamlit as st

backend_url = "http://backend:8000"

# Function to get logged user info
def get_user_info(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{backend_url}/v1/users/me", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch user info")
        return None
    
# Function to get logged user appointments
def get_user_appointments(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{backend_url}/v1/appointments", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Function to get all appointments
def get_all_appointments(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{backend_url}/v1/appointments/all", headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return []  # Return an empty list if no appointments are found
    else:
        st.error(
            f"Failed to fetch appointments: {response.json().get('detail', 'Unknown error')}"
        )
        return []

# Function to get all appointments for a specific phone number
def get_appointments_by_phone(token, phone):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{backend_url}/v1/admin/appointments/phone/{phone}", headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Function to get all appointments for a spesific month and year
def get_appointments_by_month_year(token, month, year):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{backend_url}/v1/admin/appointments/month/{month}/year/{year}",
        headers=headers,
    )
    if response.status_code == 200:
        return response.json()
    else:
        return []
    
# Function to delete appointment
def delete_appointment(token, appointment_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(
        f"{backend_url}/v1/appointments/{appointment_id}", headers=headers
    )
    if response.status_code == 200:
        st.success("Appointment deleted successfully")
    else:
        st.error("Failed to delete appointment")
        
# Function to update appointment
def update_appointment(token, appointment_id, appointment_data):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(f"{backend_url}/v1/appointments/{appointment_id}", json=appointment_data, headers=headers)
    return response

# Function to get all users
def get_all_users(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{backend_url}/v1/admin/users", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(
            f"Failed to fetch users: {response.json().get('detail', 'Unknown error')}"
        )
        return []


# Function to delete user
def delete_user(token, phone):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{backend_url}/v1/admin/users/{phone}", headers=headers)
    if response.status_code == 200:
        st.success(f"User with phone {phone} deleted successfully")
    else:
        st.error(f"Failed to delete user with phone {phone}")
