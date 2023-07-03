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
    url_weather=f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&units=metric"
    response_2=requests.get(url_weather)
    data_2=response_2.json()
    weather.append(data_2['weather'][0]['main'])
    temp.append(data_2['main']['temp'])
    temp_min.append(data_2['main']['temp_min'])
    temp_max.append(data_2['main']['temp_max'])
    humidity.append(data_2['main']['humidity'])
    city.append(location_name)

streamlit.title('Weather Data & Trends Dashboard')
streamlit.header('🌁Current city temperature and weather 🌃')
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

def color_background(value):
    if value >= 30:
        color = "lightcoral"
    elif value < 30 and value > 15:
        color = "lemonchiffon"
    else:
        color = "lightskyblue"
    return f'background-color: {color}'

streamlit.dataframe(df.style.applymap(color_background, subset=['temp', 'temp_min', 'temp_max']))




def get_history_weather_info(location_name):
    api_key='0d4be18c209e1127a2eb7dca54706dfa'
    url_coordinates=f"http://api.openweathermap.org/geo/1.0/direct?q={location_name}&limit=1&appid={api_key}"
    response_1=requests.get(url_coordinates)
    data_1=response_1.json()
    lat=data_1[0]["lat"]
    lon=data_1[0]["lon"]
    url_weather=f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
    response_2=requests.get(url_weather)
    data_2=response_2.json()
    list_datetime=[]
    list_temp_min=[]
    list_temp_max=[]
    for i in range(0,len(data_2['list'])):
        list_datetime.append(data_2['list'][i]['dt_txt'])
        list_temp_min.append(data_2['list'][i]['main']['temp_min'])
        list_temp_max.append(data_2['list'][i]['main']['temp_max'])
    keys=list_datetime
    keys_2=['temp_min', 'temp_max']
    dic_forecast={}
    for i in keys:
        for j in keys_2:
            key=(i,j)
            dic_forecast[key]=None
    list_minmax = [val for pair in zip(list_temp_min, list_temp_max) for val in pair]
    for index, key in enumerate(dic_forecast):
        dic_forecast[key]=list_minmax[index]
    dic_filtered={key: value for key, value in dic_forecast.items() if '09:00:00' in key[0]}
    modified_dict = {}
    for key, value in dic_filtered.items():
        modified_key = (key[0].split()[0], key[1])
        modified_dict[modified_key] = value
    single_df = pd.DataFrame(modified_dict.values(), index=pd.MultiIndex.from_tuples(modified_dict.keys()))
    single_df = single_df.rename(columns={0: location_name})
    return single_df
    
cities_selected_2=streamlit.multiselect("Pick some cities: ", city_choice, ['Bandon', 'Bend'])

concatenated_df = pd.DataFrame()

for city in cities_selected_2:
    temp_df=get_history_weather_info(city)
    concatenated_df=pd.concat([temp_df, concatenated_df], axis=1)

streamlit.dataframe(concatenated_df.style.applymap(color_background))
