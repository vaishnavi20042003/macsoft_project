from tkinter import *
from tkinter import ttk
from tkinter import ttk,messagebox
import tkinter as tk
from tkinter import filedialog
import platform
import psutil
import time

#brightness
import screen_brightness_control as pct

#audio
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#weather
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

#clock
from time import strftime

#calendar
from tkcalendar import *

#open google
import pyautogui

import subprocess
import webbrowser as wb
import random

root=Tk()
root.title('mac-soft Tool')
root.geometry("850x500+300+170")
root.resizable(False,False)
root.configure(bg='#292e2e')



#icon
image_icon=PhotoImage(file="C:\\Users\\vaish\\OneDrive\\Desktop\\Gui with tkinter\\Image\\icon.png.png")
root.iconphoto(False,image_icon)

Body=Frame(root,width=900,height=600,bg="#d6d6d6")
Body.pack(pady=20,padx=20)


LHS=Frame(Body,width=310,height=435,bg="#f4f5f5",highlightbackground="#adacb1",highlightthickness=1)
LHS.place(x=10,y=10)

#logo

photo=PhotoImage(file="C:\\Users\\vaish\\OneDrive\\Desktop\\Gui with tkinter\\Image\\lapi.png")
myimage=Label(LHS,image=photo,background="#f4f5f5")
myimage.place(x=2,y=20)

my_system=platform.uname()
l1=Label(LHS,text=my_system.node,bg="#f4f5f5",font=("Acumin Variable Concept",10,'bold'),justify="center")
l1.place(x=70,y=200)

l2=Label(LHS,text=f"Version:{my_system.version}",bg="#f4f5f5",font=("Acumin Variable Concept",8),justify="center")
l2.place(x=50,y=225)

l3=Label(LHS,text=f"System:{my_system.system}",bg="#f4f5f5",font=("Acumin Variable Concept",8),justify="center")
l3.place(x=15,y=250)

l4=Label(LHS,text=f"Machine:{my_system.machine}",bg="#f4f5f5",font=("Acumin Variable Concept",9),justify="center")
l4.place(x=15,y=275)

l5=Label(LHS,text=f"Total RAM installed:{round(psutil.virtual_memory().total/1000000000,2)} GB",bg="#f4f5f5",font=("Acumin Variable Concept",10,"bold"),justify="center")
l5.place(x=12,y=295)

l6=Label(LHS,text=f"Processor:{my_system.processor}",bg="#f4f5f5",font=("Acumin Variable Concept",6,"bold"),justify="center")
l6.place(x=5,y=320)

##############################################

RHS=Frame(Body,width=470,height=230,bg="#f4f5f5",highlightbackground="#adacb1",highlightthickness=1)
RHS.place(x=330,y=10)

system=Label(RHS,text="System",font=("Acumin Variable concept",10,"bold","underline"),bg="#f4f5f5")
system.place(x=10,y=10)

##########BATTERY#########

def convertTime(seconds):
    minutes,seconds=divmod(seconds,60)
    hours,minutes=divmod(minutes,60)
    return "%d:%02d:%02d"% (hours,minutes,seconds)


def none():
    global battery_png
    global battery_label
    battery=psutil.sensors_battery()
    if battery is None:
        lb1.config(text="No Battery Detected")
        lb1_plug.config(text="Plug in: N/A")
        lb1_time.config(text="N/A")
    else:
        percent=battery.percent
        time=convertTime(battery.secsleft)

    lb1.config(text=f"{percent}%")
    lb1_plug.config(text=f'Plug in:{str(battery.power_plugged)}')
    lb1_time.config(text=f'{time} remaining')


    battery_label=Label(RHS,background="#f4f5f5")
    battery_label.place(x=5,y=15)

    lb1.after(1000,none)

    if battery.power_plugged==True:
        battery_png=PhotoImage(file="C:\\Users\\vaish\\OneDrive\\Desktop\\Gui with tkinter\\Image\\charging1.png")
        battery_label.config(image=battery_png)

    else:
        battery_png=PhotoImage(file="C:\\Users\\vaish\\OneDrive\\Desktop\\Gui with tkinter\\Image\\battery1.png")
        battery_label.config(image=battery_png)

lb1=Label(RHS,font=("Acumin Variable concept",25,"bold"),bg="#f4f5f5")
lb1.place(x=200,y=40)

lb1_plug=Label(RHS,font=("Acumin Variable concept",10),bg="#f4f5f5")
lb1_plug.place(x=20,y=90)

lb1_time=Label(RHS,font=("Acumin Variable concept",12),bg="#f4f5f5")
lb1_time.place(x=150,y=90)

none()
##########SPEAKER########

lb1_speaker=Label(RHS,text="Speaker:",font=('arial',10,"bold"),bg="#f4f5f5")
lb1_speaker.place(x=10,y=150)
volume_value=tk.DoubleVar()

def get_current_volume_value():
    return "{: .2f}".format(volume_value.get())

def volume_changed(event):
    device=AudioUtilities.GetSpeakers()
    interface= device.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
    volume=cast(interface,POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(-float(get_current_volume_value()),None)

style=ttk.Style()
style.configure("TScale",background="#f4f5f5")

volume=ttk.Scale(RHS,from_=60,to=0,orient="horizontal",command=volume_changed,variable=volume_value)
volume.place(x=90,y=150)
volume.set(20)


#############BRIGHTNESS#############

lb1_brightness=Label(RHS,text="Brightness:",font=('arial',10,"bold"),bg="#f4f5f5")
lb1_brightness.place(x=10,y=190)

current_value=tk.DoubleVar()

def get_current_value():
    return "{: .2f}".format(current_value.get())

def brightness_changed(event):
    pct.set_brightness(get_current_value())

brightness=ttk.Scale(RHS,from_=0,to=100,orient="horizontal",command=brightness_changed,variable=current_value)
brightness.place(x=110,y=190)

#######################

def weather():
    app1=Toplevel()
    app1.geometry("850x500+300+170")
    app1.title("Weather")
    app1.configure(bg="#f4f5f5")
    app1.resizable(False,False)

    #icon
    image_icon=PhotoImage(file="C:\\Users\\vaish\\OneDrive\\Desktop\\Gui with tkinter\\Image\\a1weather.png")
    app1.iconphoto(False,image_icon)

    def getWeather():
        try:
            city=textfield.get()

            geolocator=Nominatim(user_agent="geoapiExercises")
            location=geolocator.geocode(city)
            if location is None:
                messagebox.showerror("Weather App", "Could not locate the city. Please try again.")
                return

            obj=TimezoneFinder()
            result=obj.timezone_at(lng=location.longitude,lat=location.latitude)

            home=pytz.timezone(result)
            local_time=datetime.now(home)
            current_time=local_time.strftime("%I:%M %p")
            clock.config(text=current_time)
            name.config(text="CURRENT WEATHER")

            API_key = '55dd068db33e84616fc2c6a2c7663088'
            api = f"https://api.openweathermap.org/data/2.5/weather?q"+city+"&appid=55dd068db33e84616fc2c6a2c7663088"
            json_data= requests.get(api).json()

            condition=json_data['weather'][0]['main']
            description=json_data['weather'][0]['description']
            temp=int(json_data["main"]['temp']-273.15)
            pressure=json_data['main']['pressure']
            humidity=json_data['main']['humidity']
            wind=json_data['main']['speed']

            t.config(text=(temp,"°"))
            c.config(text=(condition,"|",'FEELS',"LIKE",temp,'°'))

        except Exception as e:
            print(f"An error occurred: {e}")
            messagebox.showerror("Weather App", "An error occurred. Please check your city name or network connection.")

    #search box
    Search_image=PhotoImage(file="C:\\Users\\vaish\\OneDrive\\Desktop\\Gui with tkinter\\Image\\search_bar.png")
    myimage=Label(app1,image=Search_image,bg="#f4f5f5")
    myimage.place(x=20,y=20)

    textfield=tk.Entry(app1,justify="center",width=17,font=("poppins",25,"bold"),bg="#404040",border=0,fg="white")
    textfield.place(x=30,y=30)
    textfield.focus()

    Search_icon=PhotoImage(file="C:\\Users\\vaish\\OneDrive\\Desktop\\Gui with tkinter\\Image\\searchbox.png")
    myimage_icon=Button(app1,image=Search_icon,borderwidth=0,cursor="hand2",bg="#404040",command=getWeather)
    myimage_icon.place(x=360,y=20)

    #bottom box
    Frame_image=PhotoImage(file="C:\\Users\\vaish\\OneDrive\\Desktop\\Gui with tkinter\\Image\\bluebox12.png")
    frame_myimage=Label(app1,image=Frame_image,bg="#f4f5f5")
    frame_myimage.pack(padx=5,pady=5,side=BOTTOM)

    #time
    name=Label(app1,font=('arial',15,"bold"),bg="#f4f5f5")
    name.place(x=30,y=100)
    clock=Label(app1,font=('Helvetica',20),bg="#f4f5f5")
    clock.place(x=30,y=130)

    #label
    label1=Label(app1,text="WIND",font=('Helvetica',15,"bold"),fg="black",bg="white")
    label1.place(x=90,y=270)

    label2=Label(app1,text="HUMIDITY",font=('Helvetica',15,"bold"),fg="black",bg="white")
    label2.place(x=220,y=270)

    label3=Label(app1,text="DESCRIPTION",font=('Helvetica',15,"bold"),fg="black",bg="white")
    label3.place(x=390,y=270)

    label4=Label(app1,text="PRESSURE",font=('Helvetica',15,"bold"),fg="black",bg="white")
    label4.place(x=640,y=270)

    t=Label(app1,font=("arial",70,'bold'),fg="#ee666d",bg="#f4f5f5")
    t.place(x=400,y=150)
    c=Label(app1,font=("arial",70,'bold'),bg="#f4f5f5")
    c.place(x=400,y=250)

    w=Label(app1,text="...",font=("arial",20,"bold"),bg="white")
    w.place(x=120,y=430)
    h=Label(app1,text="...",font=("arial",20,"bold"),bg="white")
    h.place(x=280,y=430)
    d=Label(app1,text="...",font=("arial",20,"bold"),bg="white")
    d.place(x=450,y=430)
    p=Label(app1,text="...",font=("arial",20,"bold"),bg="white")
    p.place(x=670,y=430)


    app1.mainloop()


def clock():
    app2=Toplevel()
    app2.geometry("850x110+300+10")
    app2.title("Clock")
    app2.configure(bg="#292e2e")
    app2.resizable(False,False)

    #icon
    image_icon=PhotoImage(file="C:\\Users\\vaish\\OneDrive\\Desktop\\Gui with tkinter\\Image\\ap2clock.png")
    app2.iconphoto(False,image_icon)

    def clock():
        text=strftime('%H:%M:%S %p')
        lb1.config(text=text)
        lb1.after(1000,clock)

    lb1=Label(app2,font=('digital-7',45,'bold'),width=20,bg="#f4f5f5",fg="#292e2e")
    lb1.pack(anchor='center',pady=20)
    clock()

    app2.mainloop()

def calendar():
    app3=Toplevel()
    app3.geometry("300x300+-10+10")
    app3.title("Calendar")
    app3.configure(bg="grey")
    app3.resizable(False,False)

    #icon
    image_icon=PhotoImage(file="C:\\Users\\vaish\\OneDrive\\Desktop\\Gui with tkinter\\Image\\ap3calendar.png")
    app3.iconphoto(False,image_icon)

    mycal=Calendar(app3,setmode='day',date_pattern='d/m/yy')
    mycal.pack(padx=15,pady=35)

    app3.mainloop()

def screenshot():
    root.iconify()
    time.sleep(0.5)
    myScreenshot=pyautogui.screenshot()
    file_path=filedialog.asksaveasfilename(defaultextension='.png')
    if file_path:  # If the user provided a file path, save the screenshot
        myScreenshot.save(file_path)
    root.deconify()

def chrome():
    wb.register('chrome',None)
    wb.open('https://www.google.com/')
#----------------------------------------------------------------
RHB=Frame(Body,width=470,height=190,bg="#f4f5f5",highlightbackground="#adacb1",highlightthickness=1)
RHB.place(x=330,y=255)

apps=Label(RHB,text="Apps",font=("Acumin Variable Concept",15),bg="#f4f5f5")
apps.place(x=10,y=10)

app1_image=PhotoImage(file="C:\\Users\\vaish\\OneDrive\\Desktop\\Gui with tkinter\\Image\\a1weather.png")
app1=Button(RHB,image=app1_image,bd=0,command=weather)
app1.place(x=15,y=50)

app2_image=PhotoImage(file="C:\\Users\\vaish\\OneDrive\\Desktop\\Gui with tkinter\\Image\\ap2clock.png")
app2=Button(RHB,image=app2_image,bd=0,command=clock)
app2.place(x=100,y=50)

app3_image=PhotoImage(file="C:\\Users\\vaish\\OneDrive\\Desktop\\Gui with tkinter\\Image\\ap3calendar.png")
app3=Button(RHB,image=app3_image,bd=0,command=calendar)
app3.place(x=185,y=50)

app4_image=PhotoImage(file="C:\\Users\\vaish\\OneDrive\\Desktop\\Gui with tkinter\\Image\\app4camera.png")
app4=Button(RHB,image=app4_image,bd=0,command=screenshot)
app4.place(x=270,y=50)

app5_image=PhotoImage(file="C:\\Users\\vaish\\OneDrive\\Desktop\\Gui with tkinter\\Image\\ap5google.png")
app5=Button(RHB,image=app5_image,bd=0,command=chrome)
app5.place(x=355,y=50)


root.mainloop()
