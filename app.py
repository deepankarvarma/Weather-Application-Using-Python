import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# OpenWeatherMap API key
# API_KEY = '<your-api-key>'
st.set_page_config(
    page_title="Weather Application",
    page_icon=":sunny:",
    # layout="wide",
    # initial_sidebar_state="expanded",
)
st.title('Weather Application')
st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://4kwallpapers.com/images/wallpapers/texture-dark-background-purple-4480x2520-3086.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
# Ask for city name
city = st.text_input('Enter a city name:')

if city:
    # Make API request for current weather
    vs=True
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={st.secrets["API_KEY"]}&units=metric&lang=en'
    response = requests.get(url)
    data = response.json()

    # Display current weather
    if data['cod'] == 200:
        st.markdown(f"<h3>Current weather in {city}:</h3>", unsafe_allow_html=True)
        st.markdown(f"<b>Description:</b> {data['weather'][0]['description']}", unsafe_allow_html=True)
        st.markdown(f"<b>Temperature:</b> {data['main']['temp']}°C", unsafe_allow_html=True)
        st.markdown(f"<b>Humidity:</b> {data['main']['humidity']}%", unsafe_allow_html=True)
        st.markdown(f"<b>Wind Speed:</b> {data['wind']['speed']} m/s", unsafe_allow_html=True)
    else:
        st.write('City not found')
        vs=False

    if vs :# Make API request for 24-hour forecast
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=en'
        response = requests.get(url)
        data = response.json()

        # Prepare data for tabular and graphical display
        df = pd.json_normalize(data['list'])
        df['datetime'] = pd.to_datetime(df['dt_txt'])
        df = df[['datetime', 'main.temp']]
        df.set_index('datetime', inplace=True)
        df = df[df.index < pd.Timestamp.now() + pd.Timedelta(hours=24)]
        df = df.resample('3H').asfreq().interpolate()

        # Display 24-hour forecast table
        st.markdown(f"<h3>24-hour forecast for {city}:</h3>", unsafe_allow_html=True)
        st.write(df)

        # Display 24-hour forecast chart
        fig, ax = plt.subplots()
        ax.plot(df)
        ax.set_xlabel('Time')
        ax.set_ylabel('Temperature (°C)')
        ax.set_title(f"24-hour forecast for {city}")
        ax.set_xticklabels(df.index.strftime('%m-%d %H:%M'), rotation=45)
        st.pyplot(fig)

