import streamlit as st
from helpers.render_functions import render_appointment
from helpers.pagination import expander_with_pagination
from helpers.api_requests import get_user_info, get_user_appointments


def profile_page():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please log in to access this page")
        return

    st.subheader("My Profile")

    # Initialize expander state
    if "expander_open" not in st.session_state:
        st.session_state["expander_open"] = False

    # Initialize pagination
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = 1

    user_info = get_user_info(st.session_state["token"])
    if user_info:
        st.write(f"**Full Name:** {user_info['full_name']}")
        st.write(f"**Phone:** {user_info['phone']}")
        st.write(f"**Email:** {user_info['email']}")
        st.write(f"**Role:** {user_info['role']}")

        # Check if the user is an admin and show the Admin Actions button
        if user_info["role"] == "admin":
            if st.button("Admin Actions"):
                st.session_state["expander_open"] = False
                st.session_state["current_page"] = 1
                st.session_state["page"] = "Admin Actions"
                st.rerun()

    st.divider()

    st.subheader("My Appointments")

    # Get current logged user's appointments and display then in an expandable list with pages
    appointments = get_user_appointments(st.session_state["token"])
    expander_with_pagination(
        "Show My Appointments",
        appointments,
        render_appointment,
        "expander_open",
        "current_page",
    )

    st.divider()

    if st.button("Back to Main Page"):
        st.session_state["page"] = "Main Page"
        st.session_state["current_page"] = 1
        st.session_state["expander_open"] = False
        st.rerun()


if __name__ == "__main__":
    profile_page()
