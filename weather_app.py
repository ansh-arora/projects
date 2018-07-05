import datetime
import json
import urllib.request
from tkinter import *
import requests
import re

i=0
def url_builder(city_name):
    user_api = 'cc16b20fbaa6f86f4708777632b093b9'  # Obtain yours form: http://openweathermap.org/
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    api = 'http://api.openweathermap.org/data/2.5/weather?q='     # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz

    full_api_url = api + str(city_name) + '&mode=json&units=' + unit + '&APPID=' + user_api
    return full_api_url
# # http://api.openweathermap.org/data/2.5/weather?id=1273294&mode=json&units=metric&APPID=xxxxxxxxxxxxxx

def data_fetch(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict
#
def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time

def data_organizer(raw_api_dict):
    data = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        temp=raw_api_dict.get('main').get('temp'),
        temp_max=raw_api_dict.get('main').get('temp_max'),
        temp_min=raw_api_dict.get('main').get('temp_min'),
        humidity=raw_api_dict.get('main').get('humidity'),
        pressure=raw_api_dict.get('main').get('pressure'),
        sky=raw_api_dict['weather'][0]['main'],
        sunrise=time_converter(raw_api_dict.get('sys').get('sunrise')),
        sunset=time_converter(raw_api_dict.get('sys').get('sunset')),
        wind=raw_api_dict.get('wind').get('speed'),
        wind_deg=raw_api_dict.get('deg'),
        dt=time_converter(raw_api_dict.get('dt')),
        cloudiness=raw_api_dict.get('clouds').get('all')
    )
    return data

def url_builder2(city_name):
    user_api = 'cc16b20fbaa6f86f4708777632b093b9'  # Obtain yours form: http://openweathermap.org/
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    api = 'http://api.openweathermap.org/data/2.5/forecast?q='  # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz
    full_api_url = api + str(city_name) + '&mode=json&units=' + unit + '&APPID=' + user_api
    r = requests.get(url=full_api_url)
    json_data= r.json()
    list_items= json_data['list']
    return list_items

next_days=[]
def data_sep(list_items):
    next_days = []
    for items in list_items:
        matchObj = re.match(r"((\d+)-(\d+)-(\d+)) (00:00:00)",items['dt_txt'], re.M | re.I)
        if matchObj:
            next_days.append(items)
    return next_days

def data_organizer2(raw_list):
    data = dict(
        date=raw_list[i]['dt_txt'],
        temp=raw_list[i]['main']['temp'],
        temp_max=raw_list[i]['main']['temp_max'],
        temp_min=raw_list[i]['main']['temp_min'],
        humidity=raw_list[i]['main']['humidity'],
        pressure=raw_list[i]['main']['pressure'],
        sky=raw_list[i]['weather'][0]['main'],
        wind=raw_list[i]['wind']['speed'],
        wind_deg=raw_list[i]['wind']['deg'],
        dt=time_converter(raw_list[i]['dt']),
        cloudiness=raw_list[i]['clouds']['all']
    )
    return data

def data_output2(data):

    temp_value.config(text=str(data['temp']) + '\xb0' + 'C'+'  @  00:00:00')

    temp_max.config(text=str(data['temp_max']) + '\xb0' + 'C')

    temp_min.config(text=str(data['temp_min']) + '\xb0' + 'C')

    previous.config(state=NORMAL,command=previous_button)

def next_button():
    global i
    i=i+1
    if i==3:
        next.config(state=DISABLED)
    city = city_entry.get()
    data_output2(data_organizer2(data_sep(url_builder2(city))))

def data_output(data):

        city_lab = Label(m, text="City:")
        city_lab.grid(row=5, column=0)
        city_data.config(text=data['city']+','+data['country'])
        city_data.grid(row=5, column=1)

        cur_temp = Label(m,text='Current Temperature:')
        cur_temp.grid(row=6,column=0)
        temp_value.config(text=str(data['temp'])+'\xb0' + 'C')
        temp_value.grid(row=6,column=1)
        temp_max_label=Label(m,text='Max Temperature:')
        temp_max_label.grid(row=7,column=0)
        temp_max.config(text=str(data['temp_max']) + '\xb0' + 'C')
        temp_max.grid(row=7, column=1)
        temp_min_label = Label(m, text='Min Temperature:')
        temp_min_label.grid(row=8, column=0)
        temp_min.config(text=str(data['temp_min']) + '\xb0' + 'C')
        temp_min.grid(row=8, column=1)
        next.config(text='Next Day>>',command=next_button)
        next.grid(row=9,column=3)
        previous.config(text='<<Previous Day',state=DISABLED)
        previous.grid(row=9,column=1)

def previous_button():
    global i
    if i==0:
        city_name = city_entry.get()
        data_output(data_organizer(data_fetch(url_builder(city_name))))

    else:
        i=i-1
        city = city_entry.get()
        data_output2(data_organizer2(data_sep(url_builder2(city))))
        next.config(state=NORMAL)

try:
    m = Tk(className='Weather Forecast')
    city_label = Label(m,text="Enter a city: ")
    city_label.grid(row=0,column=0)
    city_entry = Entry(m)
    city_entry.grid(row=0,column=1)
    city_data = Label(m)
    country_data= Label(m)
    temp_value=Label(m)
    temp_max = Label(m)
    temp_min = Label(m)
    show = Button(m,text="Show",command=previous_button)
    show.grid(row=1, column=1)
    next=Button(m)
    previous=Button(m)
    m.mainloop()
except IOError:
    print('no internet')

























