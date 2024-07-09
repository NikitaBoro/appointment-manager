import streamlit as st
from datetime import datetime, timedelta
from helpers.api_requests import get_all_appointments, update_appointment


# Function to generate a list of the next 100 days
def generate_date_options(appointment_date):
    today = datetime.today()
    appointment_date_obj = datetime.strptime(appointment_date, "%d-%m-%Y").date()

    # Get the earliest date between today and the appointment date
    start_date = min(today.date(), appointment_date_obj)

    # Generate dates for the next 100 days from the start date
    date_options = [start_date + timedelta(days=i) for i in range(101)]

    # Convert the dates to the required string format
    date_options_str = [date.strftime("%d-%m-%Y") for date in date_options]

    # Ensure the appointment date is included
    if appointment_date not in date_options_str:
        date_options_str.append(appointment_date)

    return date_options_str


def update_appointment_page():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please log in to access this page")
        return

    appointment = st.session_state.get("selected_appointment")
    if not appointment:
        st.warning("No appointment selected")
        return

    st.subheader(
        f"Update Appointment for {appointment['date']} at {appointment['time']}"
    )

    service_options = ["Manicure", "Pedicure", "Haircut"]
    time_slots = [f"{hour:02d}:00" for hour in range(8, 23)]
    date_options = generate_date_options(appointment["date"])

    # Get all appointments
    all_appointments = get_all_appointments(st.session_state["token"])

    # Selected date for the appointment
    new_date = st.selectbox(
        "Date", date_options, index=date_options.index(appointment["date"])
    )

    # Filter appointments for the selected date
    existing_appointments = [a for a in all_appointments if a["date"] == new_date]

    # Filter out the taken time slots
    taken_time_slots = [a["time"] for a in existing_appointments]
    available_time_slots = [slot for slot in time_slots if slot not in taken_time_slots]

    # Filter out past time slots
    current_time = datetime.now().time()
    selected_date_obj = datetime.strptime(new_date, "%d-%m-%Y").date()
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
        st.warning("No available time slots for this date")
    else:
        service = st.selectbox(
            "Service",
            service_options,
            index=service_options.index(appointment["service"]),
        )
        time_slot = st.selectbox(
            "Time Slot",
            available_time_slots,
            index=(
                available_time_slots.index(appointment["time"])
                if appointment["time"] in available_time_slots
                else 0
            ),
        )

        if st.button("Update Appointment"):
            updated_data = {
                "id": appointment["id"],
                "name": appointment["name"],
                "phone": appointment["phone"],
                "date": new_date,
                "time": time_slot,
                "service": service,
            }
            response = update_appointment(
                st.session_state["token"], appointment["id"], updated_data
            )
            if response.status_code == 200:
                st.success("Appointment updated successfully")
                st.session_state["page"] = "Profile"
                st.rerun()
            else:
                st.error(
                    f"Failed to update appointment: {response.json().get('detail', 'Unknown error')}"
                )

    if st.button("Back to Profile"):
        st.session_state["page"] = "Profile"
        st.rerun()


if __name__ == "__main__":
    update_appointment_page()
