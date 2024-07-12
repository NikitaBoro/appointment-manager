import streamlit as st
import requests
from helpers.api_requests import backend_url


def login_page():
    st.text("Please login or register to schedule appointments")
    st.subheader("Login")
    phone = st.text_input("Phone")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not phone or not password:
            st.error("Missing phone or password")
        else:
            response = requests.post(
                f"{backend_url}/v1/user/token",
                data={"username": phone, "password": password},
            )
            if response.status_code == 200:
                token = response.json()["access_token"]
                if token:
                    st.session_state["token"] = token
                    st.session_state["logged_in"] = True
                    st.session_state["phone"] = phone
                    st.session_state["page"] = "Main Page"
                    st.rerun()
            else:
                st.error(f"Login failed: {response.json()['detail']}")

    if st.button("Register"):
        st.session_state["page"] = "Register"
        st.rerun()
