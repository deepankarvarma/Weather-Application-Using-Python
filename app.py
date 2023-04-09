import streamlit as st
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

API_KEY = ''

def get_weather_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

def plot_chart(weather_data):
    fig, ax = plt.subplots()
    dates = []
    temps = []
    for forecast in weather_data["list"]:
        date_str = forecast["dt_txt"]
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        if date.hour == 12:
            dates.append(date)
            temp = forecast["main"]["temp"]
            temps.append(temp)
    ax.plot(dates, temps, label="Temperature (°C)")
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    st.pyplot(fig)

st.title("7-Day Weather Forecast")

city = st.text_input("Enter city name")
if st.button("Get Forecast"):
    weather_data = get_weather_forecast(city)
    if weather_data["cod"] == "200":
        plot_chart(weather_data)
    else:
        st.write("City not found.")
