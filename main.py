import streamlit as st

import db
import home

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
        db.load_db()
        home.app()

    run()