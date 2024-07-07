import streamlit as st
import requests
from helpers.api_requests import backend_url


def register_page():
    st.subheader("Register")
    phone = st.text_input("Phone")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2, col3 = st.columns([3, 2, 1])
    with col3:
        if st.button("Back"):
            st.session_state["page"] = "Login"
            st.rerun()

    with col1:
        if st.button("Register"):
            # Validate input fields
            if not phone:
                st.error("Phone is required")
                return
            if not phone.isdigit() or len(phone) != 10:
                st.error("Phone number must be 10 digits long")
                return
            if not full_name:
                st.error("Full Name is required")
                return
            if not email:
                st.error("Email is required")
                return
            if not password:
                st.error("Password is required")
                return
            if "@" not in email or "." not in email:
                st.error("Invalid email address")
                return

            # Registration request
            response = requests.post(
                f"{backend_url}/v1/register",
                json={
                    "phone": phone,
                    "full_name": full_name,
                    "email": email,
                    "role": "user",
                },
                params={"password": password},
            )
            if response.status_code == 200:
                st.success("Registration successful")
                st.session_state["page"] = "Login"
                st.rerun()
            else:
                st.error(f"Registration failed: {response.json()['detail']}")


if __name__ == "__main__":
    register_page()
