import streamlit as st
from db import match_password, register_user
import re

# User authentication app, handling login and registration
def authenticate():
    # Initialize session state for tracking authentication
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    # Give the user the option to either login or register
    auth_choice = st.selectbox("Select an option", ["Login", "Register"])

    # Registration flow
    if auth_choice == "Register":
        username = st.text_input("Enter your username")
        password = st.text_input("Enter a password", type="password")
        confirm_password = st.text_input("Confirm your password", type="password")

        if st.button("Register"):
            if len(username) < 4:
                st.error("Username must be larger than 4 characters!")

            password_strength_issue = password_strength(password)
            if password_strength_issue:
                st.error(password_strength_issue)
                return
            if password != confirm_password:
                st.error("Passwords do not match!")
                return
            else:
                try:
                    register_user(username, password)
                    st.success(f"User {username} registered successfully!")
                    # Mark the user as authenticated after successful registration
                    st.session_state['authenticated'] = True
                    # Store the username in session state
                    st.session_state['username'] = username
                except Exception as e:
                    st.error(f"An error occurred during registration: {str(e)}")

    # Login flow
    elif auth_choice == "Login":
        username = st.text_input("Enter your username")
        password = st.text_input("Enter your password", type="password")

        if st.button("Login"):
            try:
                if match_password(username, password):
                    st.success(f"Welcome back, {username}!")
                    # Mark the user as authenticated after successful login
                    st.session_state['authenticated'] = True
                    # Store the username in session state
                    st.session_state['username'] = username
                else:
                    st.error("Login failed! Incorrect username or password.")
            except Exception as e:
                st.error(f"An error occurred during login: {str(e)}")

    # If the user is authenticated, rerun the app to switch to the main app
    if st.session_state['authenticated']:
        st.rerun()

def password_strength(password):
    msg = None

    if len(password) < 8:
        msg += "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        msg += "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        msg += "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        msg += "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        msg += "Password must contain at least one special character."
    return msg  # No issues found, password is strong