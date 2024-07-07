import streamlit as st
import requests
from datetime import datetime
from helpers.api_requests import backend_url, get_all_appointments


def create_appointment_page():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please log in to access this page")
        return

    selected_date = st.session_state.get("selected_date")
    if not selected_date:
        st.warning("No date selected")
        return

    st.subheader(f"Create Appointment for {selected_date}")

    service_options = ["Manicure", "Pedicure", "Haircut"]
    time_slots = [
        f"{hour:02d}:00" for hour in range(8, 23)
    ]  # Generate time slots from 08:00 to 22:00

    # Get all appointments
    all_appointments = get_all_appointments(st.session_state["token"])

    # Filter appointments for the selected date
    existing_appointments = [
        appointment
        for appointment in all_appointments
        if appointment["date"] == selected_date
    ]

    # Filter out the taken time slots
    taken_time_slots = [appointment["time"] for appointment in existing_appointments]

    # Filter out past time slots
    current_time = datetime.now().time()
    selected_date_obj = datetime.strptime(selected_date, "%d-%m-%Y").date()
    if selected_date_obj == datetime.today().date():
        available_time_slots = [
            slot
            for slot in time_slots
            if slot not in taken_time_slots
            and datetime.strptime(slot, "%H:%M").time() > current_time
        ]
    else:
        available_time_slots = [
            slot for slot in time_slots if slot not in taken_time_slots
        ]

    if not available_time_slots:
        # If no time slots available
        st.warning("No available time slots for this date")
    else:
        # If time slots available show service and time options
        service = st.selectbox("Service", service_options)
        time_slot = st.selectbox("Time Slot", available_time_slots)

        if st.button("Create Appointment"):
            # Create an appointment
            appointment_data = {
                "id": 0,
                "name": st.session_state["user_info"]["full_name"],
                "phone": st.session_state["user_info"]["phone"],
                "date": selected_date,
                "time": time_slot,
                "service": service,
            }
            headers = {"Authorization": f"Bearer {st.session_state['token']}"}
            response = requests.post(
                f"{backend_url}/v1/appointments", json=appointment_data, headers=headers
            )
            if response.status_code == 200:
                st.success("Appointment created successfully")
                st.session_state["page"] = "Main Page"
                st.rerun()
            else:
                st.error(
                    f"Failed to create appointment: {response.json().get('detail', 'Unknown error')}"
                )

    if st.button("Back"):
        st.session_state["page"] = "Main Page"
        st.rerun()


if __name__ == "__main__":
    create_appointment_page()
