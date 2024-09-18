import streamlit as st
from auth import authenticate
from home import app as home_app
from db import load_db, close_db

def main():
    st.title("Stock Market Prediction Tool")

    load_db()  # Initialize the databases

    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    # If the user is not authenticated, prompt for username and authenticate
    if not st.session_state['authenticated']:
        authenticate()
    else:
        # Once authenticated, proceed to the app's main functionality
        st.write("You are logged in!")
        home_app(st.session_state['username'])

    close_db()

if __name__ == "__main__":
    main()
