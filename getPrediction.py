import keras
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import streamlit as st
from db import add_favorite, remove_favorite, favorite_exists_exception, favorite_not_exists_exception, get_favorites

load_model = keras.models.load_model

def app(username):
    model = load_model('Stock Predictions Model.keras')
    stock = st.text_input("Enter Stock Symbol")

    if not stock:
        st.warning("Please enter a stock symbol.")
        return

    handle_favorites(username, stock)
    data = get_stock_data(stock)

    st.subheader('Stock Data')
    st.write(data)

    # Train-test split and scaling
    data_train, data_test_scaled, scaler = preprocess_data(data)

    # Plotting
    plot_moving_averages(data)

    # Predict prices
    predict_prices(data_test_scaled, model, scaler)


def get_stock_data(stock, start='2012-01-01', end=None):
    # Fetch stock data using yfinance.
    end = end or pd.Timestamp.today().strftime('%Y-%m-%d')
    return yf.download(stock, start, end)

def preprocess_data(data):
    # Preprocess data by splitting into training and scaling
    data_train = pd.DataFrame(data.Close[0:int(len(data) * 0.80)])
    data_test = pd.DataFrame(data.Close[int(len(data) * 0.80):])
    past_100_days = data_train.tail(100)
    data_test = pd.concat([past_100_days, data_test], ignore_index=True)

    scaler = MinMaxScaler(feature_range=(0, 1))
    data_test_scaled = scaler.fit_transform(data_test)

    return data_train, data_test_scaled, scaler

def plot_moving_averages(data):
    # Plot stock price with moving averages
    ma_50 = data.Close.rolling(50).mean()
    ma_100 = data.Close.rolling(100).mean()
    ma_200 = data.Close.rolling(200).mean()

    st.subheader('Price vs Moving Averages (50, 100, 200)')
    fig = plt.figure(figsize=(10, 6))
    plt.plot(data.Close, 'g', label='Price')
    plt.plot(ma_50, 'r', label='MA 50')
    plt.plot(ma_100, 'b', label='MA 100')
    plt.plot(ma_200, 'y', label='MA 200')
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Price')
    st.pyplot(fig)


def predict_prices(data_test_scaled, model, scaler):
    # Predict stock prices and plot original vs predicted prices
    x, y = create_prediction_dataset(data_test_scaled)
    predictions = model.predict(x)

    # Rescale predictions and true values
    scale = 1 / scaler.scale_
    predictions = predictions * scale
    y = y * scale

    # Plot original vs predicted prices
    st.subheader('Original vs Predicted Price')
    fig = plt.figure(figsize=(10, 6))
    plt.plot(predictions, 'r', label='Predicted Price')
    plt.plot(y, 'g', label='Original Price')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Price')
    st.pyplot(fig)

def create_prediction_dataset(data):
    # Create dataset for making predictions
    x, y = [], []
    for i in range(100, data.shape[0]):
        x.append(data[i - 100:i])
        y.append(data[i, 0])
    return np.array(x), np.array(y)


def handle_favorites(username, stock):
    # Handle favorite stock logic: toggle favorite, show status
    favorites = get_favorites(username)
    is_favorite = stock in favorites
    star_icon = '⭐' if is_favorite else '☆'

    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button(star_icon):
            toggle_favorite(username, stock, is_favorite)
    with col2:
        st.subheader(f'Stock Data for {stock}')

def toggle_favorite(username, stock, is_favorite):
    # Toggle favorite status of the stock
    try:
        if is_favorite:
            remove_favorite(username, stock)
            st.success(f'Removed {stock} from favorites.')
        else:
            add_favorite(username, stock)
            st.success(f'Added {stock} to favorites.')
    except (favorite_exists_exception, favorite_not_exists_exception) as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


# Features to add

# 1. Give user an estimate on how much profit they make by basically reading graph, sell value - buy value, store these values so they can keep track of it, add DB