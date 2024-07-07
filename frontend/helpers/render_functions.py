import streamlit as st
from .api_requests import delete_user,delete_appointment

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
        delete_user(st.session_state["token"], user["phone"])
        st.session_state["expander_users_open"] = True
        st.rerun()


# Function to render appointment info
def render_appointment(appointment, current_page_key, state_key=None):
    st.write(f"**ID:** {appointment['id']}")
    st.write(f"**Name:** {appointment['name']}")
    st.write(f"**Phone:** {appointment['phone']}")
    st.write(f"**Date:** {appointment['date']}")
    st.write(f"**Time:** {appointment['time']}")
    st.write(f"**Service:** {appointment['service']}")
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        if st.button(
            f"Update Appointment",
            key=f"update_appointment_{appointment['id']}_{current_page_key}",
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
            delete_appointment(st.session_state["token"], appointment["id"])
            st.rerun()
