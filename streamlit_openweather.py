import streamlit
import requests
import pandas as pd

# create an empty dictionary
keys=['city', 'weather', 'temp', 'temp_min', 'temp_max', 'humidity']
my_dic={key: None for key in keys}

weather=[]
temp=[]
temp_min=[]
temp_max=[]
humidity=[]
city=[]

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
    weather.append(data_2['weather'][0]['main'])
    temp.append(data_2['main']['temp'])
    temp_min.append(data_2['main']['temp_min'])
    temp_max.append(data_2['main']['temp_max'])
    humidity.append(data_2['main']['humidity'])
    city.append(location_name)

streamlit.title('Weather Data & Trends Dashboard')
streamlit.header('🌁City temperature and weather 🌃')
city_choice=['Bandon', 'Bend', 'Cameron Park', 'Fort Collins', 'Grants Pass', 'Littleton', 'Madras', 'Medford', 'Redmond', 'Roseburg', 'Sacramento']
cities_selected=streamlit.multiselect("Pick some cities:", city_choice,['Bandon', 'Bend'])

for i in cities_selected:
    get_weather_info(i)

my_dic['weather']=weather
my_dic['temp']=temp
my_dic['temp_min']=temp_min
my_dic['temp_max']=temp_max
my_dic['humidity']=humidity
my_dic['city']=city

df=pd.DataFrame(my_dic)

def color_background(val):
    if value >= 30:
    color = "red"
    elif value < 30 and value > 15:
    color = "orange"
    else:
    color = "blue"
    return f'background-color: {color}'

streamlit.dataframe(df.style.applymap(color_background, subset=['temp', 'temp_min', 'temp_max']))
