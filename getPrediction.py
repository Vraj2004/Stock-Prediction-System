import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

import db

name = ""
def get_username():
    return name
def app(user):
    global name
    name = user
    model = load_model(r'Stock Prediction Tool\Stock Predictions Model.keras')

    stock = st.text_input("Enter Stock Symbol", "GOOG") # This needs to be changed so there is no default value

    is_favorited = stock in db.get_favorites()

    starred = st.checkbox("Star", value=is_favorited, key="star_checkbox")

    if not starred:
        db.add_favorite(stock)
        st.write(f"{stock} starred!")
    else:
        db.remove_favorite(stock)
        st.write(f"{stock} unstarred!")

    start = '2012-01-01'
    end = '2024-01-01' # Change this to current date

    data = yf.download(stock, start, end)

    st.subheader('Stock Data')
    st.write(data)

    data_train = pd.DataFrame(data.Close[0: int(len(data) * 0.80)])
    data_test = pd.DataFrame(data.Close[int(len(data) * 0.80): len(data)])

    scaler = MinMaxScaler(feature_range=(0,1))

    past_100_days = data_train.tail(100)
    data_test = pd.concat([past_100_days, data_test], ignore_index=True)
    data_test_scale = scaler.fit_transform(data_test)

    st.subheader('Price vs Moving Average 50')
    ma_50_days = data.Close.rolling(50).mean()
    fig1 = plt.figure(figsize=(8, 6))
    plt.plot(ma_50_days, 'r')
    plt.plot(data.Close, 'g')
    plt.show()
    st.pyplot(fig1)

    st.subheader('Price vs Moving Average 50 vs Moving Average 100')
    ma_100_days = data.Close.rolling(100).mean()
    fig2 = plt.figure(figsize=(8, 6))
    plt.plot(ma_50_days, 'r')
    plt.plot(ma_100_days, 'b')
    plt.plot(data.Close, 'g')
    plt.show()
    st.pyplot(fig2)

    st.subheader('Price vs Moving Average 50 vs Moving Average 100 vs Moving Average 200')
    ma_200_days = data.Close.rolling(200).mean()
    fig2 = plt.figure(figsize=(8, 6))
    plt.plot(ma_50_days, 'r')
    plt.plot(ma_100_days, 'b')
    plt.plot(data.Close, 'g')
    plt.plot(ma_200_days, 'y')
    plt.show()
    st.pyplot(fig2)

    x = []
    y = []

    for i in range(100, data_test_scale.shape[0]):
        x.append(data_test_scale[i - 100:i])
        y.append(data_test_scale[i, 0])

    x, y = np.array(x), np.array(y)

    predict = model.predict(x)

    scale = 1/scaler.scale_

    predict = predict * scale
    y = y * scale

    # CHANGE NEEDED

    # Make it in terms of years at the bottom and price on the side
    st.subheader('Original vs Predicted Price')
    fig4 = plt.figure(figsize=(8, 6))
    plt.plot(predict, 'r', label='Original Price')
    plt.plot(y, 'g', label='Predicted Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.show()
    st.pyplot(fig4)

    # Features to add

    # 1. Give user an estimate on how much profit they make by basically reading graph, sell value - buy value, store these values so they can keep track of it, add DB
    # 2. Try to save favourites and the latest data for it (Kinda similar to end of first part)
    # 3. Make the UI better