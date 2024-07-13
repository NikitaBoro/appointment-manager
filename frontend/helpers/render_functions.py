import streamlit as st
import datetime
import time
from .api_requests import delete_user, delete_appointment


# Function to render user info
def render_user(user, current_page_key):
    st.write(f"**Phone:** {user['phone']}")
    st.write(f"**Full Name:** {user['full_name']}")
    st.write(f"**Email:** {user['email']}")
    st.write(f"**Role:** {user['role']}")
    if st.button(
        f"Delete User",
        key=f"delete_user_{user['phone']}_{current_page_key}",
        type="primary",
    ):
        respone = delete_user(st.session_state["token"], user["phone"])
        if respone.status_code == 200:
            st.toast(f"User with phone {user['phone']} deleted successfully",  icon="✅")
            time.sleep(1)
            st.session_state["expander_users_open"] = True
            st.rerun()
        else:
            st.error(f"Failed to delete user with phone {user['phone']}")


# Function to render appointment info
def render_appointment(appointment, current_page_key, state_key=None):
    st.write(f"**ID:** {appointment['id']}")
    st.write(f"**Name:** {appointment['name']}")
    st.write(f"**Phone:** {appointment['phone']}")
    st.write(f"**Date:** {appointment['date']}")
    st.write(f"**Time:** {appointment['time']}")
    st.write(f"**Service:** {appointment['service']}")

    # Combine appointment date and time for comparison
    appointment_datetime = datetime.datetime.strptime(
        f"{appointment['date']} {appointment['time']}", "%d-%m-%Y %H:%M"
    )
    current_datetime = datetime.datetime.now()

    # Text for if appointment time has passed
    if appointment_datetime < current_datetime:
        st.markdown(
            "<span style='color:red'>**Status:** This appointment has passed</span>",
            unsafe_allow_html=True,
        )

    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        if st.button(
            f"Update Appointment",
            key=f"update_appointment_{appointment['id']}_{current_page_key}",
            disabled=appointment_datetime
            < current_datetime,  # Disable if appointment is in the past
        ):
            st.session_state["selected_appointment"] = appointment
            st.session_state["page"] = "Update Appointment"
            if state_key != None:
                st.session_state[state_key] = False
            st.rerun()
    with col3:
        if st.button(
            f"Delete Appointment",
            key=f"delete_appointment_{appointment['id']}_{current_page_key}",
            type="primary",
        ):
            response = delete_appointment(st.session_state["token"], appointment["id"])
            if response.status_code == 200:
                st.toast("Appointment deleted successfully",  icon="✅")
                time.sleep(1)
                st.rerun()
            else:
                st.error(
                    f"Failed to delete appointment: {response.json().get('detail', 'Unknown error')}"
                )
