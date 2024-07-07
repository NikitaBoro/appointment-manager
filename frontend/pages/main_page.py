import streamlit as st
import datetime
import calendar
from helpers.api_requests import get_user_info


def initialize_session_state():
    if "current_month" not in st.session_state:
        st.session_state["current_month"] = datetime.date.today().month
    if "current_year" not in st.session_state:
        st.session_state["current_year"] = datetime.date.today().year
    if "selected_date" not in st.session_state:
        st.session_state["selected_date"] = None


# Function to display the calendar
def show_calendar(month, year):
    st.write(f"## {calendar.month_name[month]} {year}")
    today = datetime.date.today()

    # Set Sunday as the first day of the week
    calendar.setfirstweekday(calendar.SUNDAY)

    month_calendar = calendar.monthcalendar(year, month)

    # Add day headers
    day_headers = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    header_cols = st.columns(7)
    for i, day_header in enumerate(day_headers):
        header_cols[i].write(day_header)

    for week in month_calendar:
        cols = st.columns(7)
        for day_index, day in enumerate(week):
            key = f"day-{year}-{month}-{day}"
            if day == 0:
                cols[day_index].write(" ")
            else:
                if datetime.date(year, month, day) < today:
                    cols[day_index].button(f"{day}", key=key, disabled=True)
                else:
                    if cols[day_index].button(f"{day}", key=key):
                        st.session_state["selected_date"] = (
                            f"{day:02d}-{month:02d}-{year}"
                        )
                        st.session_state["page"] = "Create Appointment"
                        st.rerun()


def main_page():
    initialize_session_state()

    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        user_info = get_user_info(st.session_state["token"])
        if user_info:
            st.session_state["user_info"] = user_info
            st.write(f"Welcome, {user_info['full_name']}")

            # My Profile button
            if st.button("My Profile"):
                st.session_state["page"] = "Profile"
                st.rerun()

            # Logout button
            if st.button("Logout", type="primary"):
                st.session_state.clear()
                st.session_state["page"] = "Login"
                st.rerun()

            st.divider()

            # Navigation buttons for previous and next months
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("Previous Month"):
                    if st.session_state["current_month"] == 1:
                        st.session_state["current_month"] = 12
                        st.session_state["current_year"] -= 1
                    else:
                        st.session_state["current_month"] -= 1

            with col3:
                if st.button("Next Month"):
                    if st.session_state["current_month"] == 12:
                        st.session_state["current_month"] = 1
                        st.session_state["current_year"] += 1
                    else:
                        st.session_state["current_month"] += 1

            # Show calendar for the current month and year in session state
            show_calendar(
                st.session_state["current_month"], st.session_state["current_year"]
            )
    else:
        st.warning("Please log in to access this page")


if __name__ == "__main__":
    main_page()
