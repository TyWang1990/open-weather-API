import streamlit
import requests

def get_weather_info(location_name):
    api_key='0d4be18c209e1127a2eb7dca54706dfa'
    url_coordinates=f"http://api.openweathermap.org/geo/1.0/direct?q={location_name}&limit=1&appid={api_key}"
    response_1=requests.get(url_coordinates)
    data_1=response_1.json()
    lat=data_1[0]["lat"]
    lon=data_1[0]["lon"]
    url_weather=f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response_2=requests.get(url_weather)
    data_2=response_2.json()
    cur_weather=data_2['weather'][0]['main']
    cur_temp=data_2['main']['temp']
    return f"The current temperature of {location_name} is: {cur_temp}°C", f"The current weather of {location_name} is: {cur_weather}"

streamlit.title('🌁 Weather Data & Trends Dashboard')
city_choice = streamlit.text_input('Which city would you like the check?', 'London')

streamlit.text(get_weather_info(city_choice)[0])
streamlit.text(get_weather_info(city_choice)[1])
