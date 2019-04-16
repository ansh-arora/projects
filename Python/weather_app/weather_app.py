import datetime
import json
import urllib.request
from tkinter import *
from tkinter import ttk
import requests
import re
from PIL import ImageTk,Image
cod=0
city1=''
country1=''
i=-1
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

def data_organizer(raw_api_dict):          #organizes data for current day
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
        cloudiness=raw_api_dict.get('clouds').get('all'),
        cod=raw_api_dict.get('cod')
    )
    global city1,country1,cod
    city1=data['city']
    country1=data['country']
    cod=data['cod']
    return data

def url_builder2(city_name):
    user_api = 'cc16b20fbaa6f86f4708777632b093b9'  # Obtain yours form: http://openweathermap.org/
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    api = 'http://api.openweathermap.org/data/2.5/forecast?q='  # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz
    full_api_url = api + str(city_name) + '&mode=json&units=' + unit + '&APPID=' + user_api
    #full_api_url returns:
    #http://api.openweathermap.org/data/2.5/forecast?q=jaipur&mode=json&units=metric&APPID=xxxxxxxxxxxxxxxxxxxx
    r = requests.get(url=full_api_url)
    json_data= r.json()
    list_items= json_data['list']
    return list_items  #returns a raw list of data of next 3 days


def data_sep(list_items):      #method to seperate data for next 3 days
    next_days = []
    for items in list_items:
        matchObj = re.match(r"((\d+)-(\d+)-(\d+)) (00:00:00)",items['dt_txt'], re.M | re.I)

        if matchObj:
            matchObj1=re.sub(r' 00:00:00',"",matchObj.group())
            if matchObj1!=str(datetime.date.today()):
                next_days.append(items)
    return next_days

def data_organizer2(raw_list):      #organize data of next 3 days
    data = dict(
        date=re.sub(r' 00:00:00',"",raw_list[i]['dt_txt']),
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

    city_label.place(x=240)
    Label(m,
          text='    ______________________________________________________________________________________________________    ',
          bg='white').place(x=195, y=70)

    canvas.place(x=435, y=110)
    if data['sky'] == 'Rain' or data['sky']=='Thunderstorm':
        img1 = Image.open('rainy.png')

    elif data['sky'] == 'Clouds':
        img1 = Image.open('cloudy.png')

    elif data['sky'] == 'Haze':
        img1 = Image.open('fog.png')

    else:
        img1 = Image.open('sunny.png')
        img1 = img1.resize((80, 80), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img1)

    canvas.create_image(0, 0, anchor=NW, image=img)
    canvas.image = img
    temp_value.config(text=str(data['temp']) + '\xb0' + 'C')
    temp_value.place(x=520, y=110)

    city_data.config(text=city1 + ',' + country1 + '\n' + data['date'] + '\n' + '"' + data['sky'] + '"')
    city_data.place(x=260, y=115)

    temp_max_min.config(
        text='Max Temperature: ' + str(data['temp_max']) + '\xb0' + 'C' + '\n' + 'Min Temperature: ' + str(
            data['temp_min']) + '\xb0' + 'C')
    temp_max_min.grid(row=8, column=1)

    humidity.config(
        text='Humidity: ' + str(data['humidity']) + '%' + '\n' + 'Pressure: ' + str(data['pressure']) + ' mb'+'\n'+'Wind Speed: '+str(data['wind'])+'km/h')
    humidity.grid(row=8, column=2)
    previous.config(state=NORMAL,command=previous_button)
    sunrise_time.config(text='Sunrise Time: ' + 'N/A' + '\n' + 'Sunset Time: ' + 'N/A')
    sunrise_time.grid(row=8, column=3)


def next_button():
    global i
    i=i+1
    if i==2:
        next.config(state=DISABLED)
    city = city_entry.get()
    data_output2(data_organizer2(data_sep(url_builder2(city))))

global img
def data_output(data):
    global cod
    if cod==200:
        city_label.place(x=220)
        Label(m,text='    ______________________________________________________________________________________________________    ',bg='white').place(x=195,y=70)

        canvas.place(x=455, y=110)
        if data['sky']=='Rain' or data['sky']=='Thunderstorm':
            img1 = Image.open('rainy.png')

        elif data['sky']=='Clouds':
            img1 = Image.open('cloudy.png')

        elif data['sky']=='Haze':
            img1 = Image.open('fog.png')

        else:
            img1 = Image.open('sunny.png')
            img1 = img1.resize((80, 80), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img1)
        canvas.create_image(0, 0, anchor=NW, image=img)
        canvas.image=img
        temp_value.config(text=str(data['temp']) + '\xb0' + 'C')
        temp_value.place(x=540, y=110)

        city_data.config(text=data['city']+','+data['country']+'\n'+'Today'+' ('+str(datetime.date.today())+')'+'\n'+'"'+data['sky']+'"')
        city_data.place(x=210,y=115)

        temp_max_min.config(text='Max Temperature: '+str(data['temp_max']) + '\xb0' + 'C'+'\n'+'Min Temperature: '+str(data['temp_min']) + '\xb0' + 'C')
        temp_max_min.grid(row=8, column=1)

        humidity.config(text='Humidity: '+str(data['humidity'])+'%'+'\n'+'Pressure: '+str(data['pressure'])+' mb'+'\n'+'Wind Speed: '+str(data['wind'])+'km/h')
        humidity.grid(row=8,column=2)

        sunrise_time.config(text='Sunrise Time: '+str(data['sunrise'])+'\n'+'Sunset Time: '+str(data['sunset']))
        sunrise_time.grid(row=8,column=3)

        next.config(text='Next Day>>',command=next_button)
        next.place(x=590,y=320)
        previous.config(text='<<Previous Day',state=DISABLED)
        previous.place(x=170,y=320)
    else:
        Label(m,text='Enter a valid city',font=('Berlin Sans FB',20),bg='white',fg='black')

def previous_button():
    global i
    if i>0:
        i=i-1
        city = city_entry.get()
        data_output2(data_organizer2(data_sep(url_builder2(city))))
        next.config(state=NORMAL)
    else:
        i=-1
        city_name = city_entry.get()
        data_output(data_organizer(data_fetch(url_builder(city_name))))



try:
    m = Tk(className=' Weather Forecast')
    m.config(bg='white')
    m.geometry("850x400")
    m.grid_columnconfigure(6, minsize=100)
    m.grid_columnconfigure(0, minsize=120)
    m.grid_rowconfigure(8, minsize=400)
    city_label = Label(m,text="Enter City: ",font=('Berlin Sans FB',15),bg='white',fg='black')
    city_label.grid(row=0,column=1)
    city_entry = Entry(m,font=('Berlin Sans FB',15),bg='white',fg='black',highlightthickness=1,highlightbackground='black')
    city_entry.grid(row=0,column=2)
    city_data = Label(m,font=('Berlin Sans FB',20),bg='white',fg='black')
    temp_value=Label(m,font=('Berlin Sans FB',40),bg='white',fg='black')
    temp_max_min = Label(m,font=('Berlin Sans FB',15),bg='white',fg='black')
    humidity=Label(m,font=('Berlin Sans FB',15),bg='white',fg='black')
    sunrise_time = Label(m,font=('Berlin Sans FB',15),bg='white',fg='black')
    show = Button(m,text="Show",command=previous_button,font=('Berlin Sans FB',15),bg='white',fg='black')
    show.grid(row=1, column=2)
    canvas = Canvas(m, width=70, height=70, bg='white', highlightbackground='white')
    next=Button(m,font=('Berlin Sans FB',15),bg='white',fg='black')
    previous=Button(m,font=('Berlin Sans FB',15),bg='white',fg='black')
    m.mainloop()
except IOError:
    print('no internet')

























