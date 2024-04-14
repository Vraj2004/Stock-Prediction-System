import streamlit as st
from streamlit_option_menu import option_menu
import app, home

st.set_page_config(
    page_title="StockApp",
)

class Mutliapp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })
    
    def run():
        with st.sidebar:
            