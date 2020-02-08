import requests
from bs4 import BeautifulSoup
import re,random
import sys
import win32gui
from datetime import datetime
import argparse
import getpass,time

#get the username
username=getpass.getuser()

#this is where all images will be saved 
#chage this if you want to save images to diffrent directory
dirc="C:\\Users\\%s\\Pictures\\"%username

nasa_url = "https://apod.nasa.gov/"
bing_url="https://bing.com"

parser = argparse.ArgumentParser()
parser.add_argument("ch",nargs='?',help="0:Nasa\n1:Bing",default=False) 
args = parser.parse_args()

#get the currnet system time 
now=datetime.now()
cur_time=now.strftime('%d_%b_%Y') 


def ask_nasa():
    print("Getting image from nasa...")
    nasa_image()

def ask_bing():
    print("Getting image from bing...")
    bing_image()

def windowswallpaper(image):
    SPI_SETDESKWALLPAPER = 20
    #set image as desktop wallpaper
    win32gui.SystemParametersInfo(SPI_SETDESKWALLPAPER, image, 3)

def nasa_image(nasa_url="https://apod.nasa.gov/"):
    try:
        page = requests.get(nasa_url)
    except requests.ConnectionError:
        print("No internet connection..\nPlease connect to internet and try again")
        print("Program will exit in 3 second")
        time.sleep(3)
        sys.exit()
    soup = BeautifulSoup(page.content, "html.parser")
    image = soup.find("img")
    nasa_url += image["src"]
    page = requests.get(nasa_url)
    filename=dirc+'nasa_'+cur_time+'.jpg'
    # Create the .jpg file
    with open(filename, "wb") as f:
        f.write(page.content)
    f.close()
    windowswallpaper(filename)

def bing_image():
    try:
        r=requests.get(bing_url)
    except requests.ConnectionError:
        print("No internet connection..\nPlease connect to internet and try again")
        print("Program will exit in 3 second")
        time.sleep(3)
        sys.exit()
    sp=BeautifulSoup(r.text,'html.parser')
    text=str(sp.find_all('meta'))
    com=re.compile(r'(https.*.jpg)')
    image=com.findall(text)
    page=requests.get(image[0])
    #create the jpg file with date
    filename=dirc+'bing_wall_'+cur_time+'.jpg'
    with open(filename ,'wb') as f:
        f.write(page.content)
    f.close()
    windowswallpaper(filename)

#if the argument is supplied 0 or 1 
#if there is no arguemnt supplied choose randomly 
if args.ch=='0':
    ask_nasa()
elif args.ch:
    ask_bing()
else:
    ch=random.choice([0,1])
    if ch==0:
        ask_nasa()
    else:
        ask_bing()
