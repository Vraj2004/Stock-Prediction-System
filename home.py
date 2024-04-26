import streamlit as st

def app():
    name = st.text_input("Enter your name")

    if name == 'Vraj':
        print('Hello')
    
