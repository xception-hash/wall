import requests
from bs4 import BeautifulSoup
#import ctypes
import re,random
import win32gui
from datetime import datetime
import argparse

#Change the extension from .pyw to .py if you want the console window
#
#If you want the program to be run at startup go to:
#C:\Users\current_user\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
#And drag the file .pyw/.py file in there
#
#If you want the program to be ran between some time periods you should use Windows Task Scheduler
#If you do not know how to check out http://theautomatic.net/2017/10/03/running-python-task-scheduler/

dirc="C:\\Users\\xception\\wallpaper\\bing_wall\\"
dirc1="C:\\Users\\xception\\wallpaper\\nasa\\"
nasa_url = "https://apod.nasa.gov/"
bing_url="https://bing.com"

parser = argparse.ArgumentParser()
parser.add_argument("ch",nargs='?',help="0:Nasa\n1:Bing",default=False) 
args = parser.parse_args()


now=datetime.now()
cur_time=now.strftime('%d_%m_%Y') 

def ask_nasa():
	print("Getting image from nasa...")
	getimage(nasa_url)

def ask_bing():
	print("Getting image from bing...")
	bing_image(bing_url)

def windowswallpaper(image):
    SPI_SETDESKWALLPAPER = 20
    win32gui.SystemParametersInfo(SPI_SETDESKWALLPAPER, image, 3)
    #use this with ctypes
    #ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image, 3)

def getimage(url):
    #Get the data from the website
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    #date = soup.findAll("p")[1].text.strip()
    image = soup.find("img")
    url += image["src"]
    page = requests.get(url)
    filename=dirc1+'nasa_'+cur_time+'.jpg'
    # Create the .jpg file
    with open(filename, "wb") as f:
        f.write(page.content)
    f.close()
    #Set the wallpaper to the .jpg file
    windowswallpaper(filename)

def bing_image(bing_url):
    r=requests.get("https://bing.com")
    sp=BeautifulSoup(r.text,'html.parser')
    text=str(sp.find_all('meta'))
    com=re.compile(r'(https.*.jpg)')
    image=com.findall(text)
    page=requests.get(image[0])
    filename=dirc+'bing_wall_'+cur_time+'.jpg'
    with open(filename ,'wb') as f:
        f.write(page.content)
    f.close()
    windowswallpaper(filename)

print(args.ch)

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




