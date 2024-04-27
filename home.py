import streamlit as st
import getPrediction

def app():
    st.header('Stock Market Predictor')
    name = st.text_input("Enter your name to continue")


    if name == "":
        st.warning("Please enter your name")
    else:
        getPrediction.app()

    
