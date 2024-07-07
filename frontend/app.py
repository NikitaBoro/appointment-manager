import streamlit as st
from pages.login import login_page
from pages.register import register_page
from pages.main_page import main_page
from pages.create_appointment import create_appointment_page
from pages.profile import profile_page
from pages.update_appointment import update_appointment_page
from pages.admin_actions import admin_actions_page


def main():
    st.title("✂️ Hair And Nail Salon 💅")


    # Determine which page to display based on session state
    page = st.session_state.get("page", "Login")

    if page == "Login":
        login_page()
    elif page == "Register":
        register_page()
    elif page == "Main Page":
        main_page()
    elif page == "Create Appointment":
        create_appointment_page()
    elif page == "Profile":
        profile_page()
    elif page == "Update Appointment":
        update_appointment_page()
    elif page == "Admin Actions":
        admin_actions_page()


if __name__ == "__main__":
    main()
