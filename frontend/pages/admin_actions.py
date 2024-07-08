import streamlit as st
from helpers.api_requests import (
    get_appointments_by_phone,
    get_appointments_by_month_year,
    get_all_users,
    get_all_appointments,
)
from helpers.render_functions import render_appointment, render_user
from helpers.pagination import expander_with_pagination


def admin_actions_page():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please log in to access this page")
        return

    token = st.session_state["token"]

    # Initialize expanders state
    expanders = ["expander_users_open", "expander_all_app_open"]
    for expander in expanders:
        if expander not in st.session_state:
            st.session_state[expander] = False

    # Initialize pagination
    pages = ["current_users_page", "current_all_app_page"]
    for page in pages:
        if page not in st.session_state:
            st.session_state[page] = 1

    # Initialize session state for appointment list when searching by phone and date
    if "show_apps_phone" not in st.session_state:
        st.session_state["show_apps_phone"] = False
    if "show_apps_m_y" not in st.session_state:
        st.session_state["show_apps_m_y"] = False

    # Callback functions that toggle the visibility of the lists
    def callback_phone():
        st.session_state["show_apps_phone"] = True
        st.session_state["show_apps_m_y"] = False

    def callback_m_y():
        st.session_state["show_apps_m_y"] = True
        st.session_state["show_apps_phone"] = False

    # Initialize session state for input values
    if "phone_num" not in st.session_state:
        st.session_state["phone_num"] = ""
    if "month" not in st.session_state:
        st.session_state["month"] = 1
    if "year" not in st.session_state:
        st.session_state["year"] = 2024

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        st.subheader("Admin Actions")
    with col3:
        if st.button("Back to Profile"):
            st.session_state["page"] = "Profile"
            st.session_state["current_users_page"] = 1
            st.session_state["expander_users_open"] = False
            st.session_state["current_all_app_page"] = 1
            st.session_state["expander_all_app_open"] = False
            st.session_state["show_apps_phone"] = False
            st.session_state["show_apps_m_y"] = False
            st.rerun()

    st.divider()

    # Get and display all users
    st.write("### All Users")
    all_users = get_all_users(token)
    expander_with_pagination(
        "Show Users",
        all_users,
        render_user,
        "expander_users_open",
        "current_users_page",
    )

    st.divider()
    # Get and display all appointments
    st.write("### All Appointments")
    all_appointments = get_all_appointments(token)
    expander_with_pagination(
        "Show All Appointments",
        all_appointments,
        render_appointment,
        "expander_all_app_open",
        "current_all_app_page",
    )

    st.divider()
    # Get appointments by phone number
    st.write("### Appointments by Phone")
    st.session_state["phone_num"] = st.text_input(
        "Enter phone number", st.session_state["phone_num"]
    )
    if st.button("Reset", key="reset_apps_by_phone"):
        st.session_state["phone_num"] = ""
        st.session_state["show_apps_phone"] = False
        st.session_state["expander_users_open"] = False
        st.session_state["expander_all_app_open"] = False
        st.rerun()

    if (
        st.button(
            "Get Appointments", key="appointments_by_phone", on_click=callback_phone
        )
        or st.session_state["show_apps_phone"]
    ):
        appointments_by_phone = get_appointments_by_phone(
            token, st.session_state["phone_num"]
        )
        if not appointments_by_phone:
            st.error(f"No appointments for phone {st.session_state['phone_num']}")
        else:
            for appointment in appointments_by_phone:
                render_appointment(appointment, "phone", "show_apps_phone")
                st.write("---")

    # Get appointments by month and year
    st.write("### Appointments by Month and Year")
    st.session_state["month"] = st.number_input(
        "Enter month (1-12)",
        min_value=1,
        max_value=12,
        step=1,
        value=st.session_state["month"],
    )
    st.session_state["year"] = st.number_input(
        "Enter year",
        min_value=2024,
        max_value=9999,
        step=1,
        value=st.session_state["year"],
    )
    if st.button("Reset", key="reset_apps_by_m_y"):
        st.session_state["month"] = 1
        st.session_state["year"] = 2024
        st.session_state["show_apps_m_y"] = False
        st.session_state["expander_users_open"] = False
        st.session_state["expander_all_app_open"] = False
        st.rerun()

    if (
        st.button("Get Appointments", key="appointments_by_date", on_click=callback_m_y)
        or st.session_state["show_apps_m_y"]
    ):
        appointments_by_month = get_appointments_by_month_year(
            token, st.session_state["month"], st.session_state["year"]
        )
        if not appointments_by_month:
            st.error(
                f"No appointments for {st.session_state['month']}/{st.session_state['year']}"
            )
        else:
            for appointment in appointments_by_month:
                render_appointment(appointment, "month_year", "show_apps_m_y")
                st.write("---")


if __name__ == "__main__":
    admin_actions_page()
