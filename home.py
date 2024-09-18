import streamlit as st
from db import get_favorites, remove_favorite, close_db
from getPrediction import app as prediction_app

def app(username):
    # Show stock prediction functionality
    prediction_app(username)
    # Display user's favorite stocks
    display_favorites(username)
    close_db()  # Close the database connection on exit

def display_favorites(username):
    # Display favorite stocks in the sidebar and provide an option to remove them.
    favorites = get_favorites(username)

    st.sidebar.header("Your favorite stocks")

    if favorites:
        for favorite in favorites:
            create_favorite_row(username, favorite)
    else:
        st.sidebar.write("No favorite stocks yet.")

def create_favorite_row(username, favorite):
    # Create a row in the sidebar for each favorite stock with a remove button.
    cols = st.sidebar.columns([3, 1])
    cols[0].write(favorite)

    if cols[1].button("Remove", key=f"remove_{favorite}"):
        handle_remove_favorite(username, favorite)

def handle_remove_favorite(username, favorite):
    # Handle removing a stock from favorites and display status messages.
    try:
        remove_favorite(username, favorite)
        st.sidebar.success(f"{favorite} removed from favorites.")
    except Exception as e:
        st.sidebar.error(f"An error occurred: {str(e)}")