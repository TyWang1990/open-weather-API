import streamlit
import requests
import pandas as pd

def get_weather_info(location_name):
    api_key='0d4be18c209e1127a2eb7dca54706dfa'
    url_coordinates=f"http://api.openweathermap.org/geo/1.0/direct?q={location_name}&limit=5&appid={api_key}"
    response_1=requests.get(url_coordinates)
    data_1=response_1.json()
    lat=data_1[0]["lat"]
    lon=data_1[0]["lon"]
    url_weather=f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response_2=requests.get(url_weather)
    data_2=response_2.json()
    cur_weather=data_2['weather'][0]['main']
    cur_temp=data_2['main']['temp']
    cur_min=data_2['main']['temp_min']
    cur_max=data_2['main']['temp_max']
    cur_hum=data_2['main']['humidity']
    
    df=pd.DataFrame(
    {
    'weather': [cur_weather],
    'temp':[cur_temp],
    'temp_min': [cur_min],
    'temp_max':[cur_max],
    'humidity':[cur_hum]
    },
    index=[location_name]
    )
    return df

streamlit.title('Weather Data & Trends Dashboard')
streamlit.header('🌁City temperature and weather 🌃')
city_choice = streamlit.text_input('Which city would you like to check?', 'London')

streamlit.dataframe(get_weather_info(city_choice))
