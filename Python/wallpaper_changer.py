import ctypes
import os
from bs4 import BeautifulSoup
import time
from urllib.error import HTTPError
import urllib.request
from urllib.request import urlretrieve
import re
import errno
import shutil
import random
import sys


def downloadImage():
    wcount = 0
    try:
        wallpaperLinks = WallpaperAddress()
        # print("1")
        for wallpaperLink in wallpaperLinks:
            # print("2")
            urldownload = fetchPhotos("http://www.santabanta.com" + wallpaperLink)
            # print(urldownload)
            # print(wcount)
            # fetchPhotos(correctlink)
            # fetchPhotos(correctlink)
            urlretrieve(urldownload, wallpapercount(wcount))
            print("Wallpaper Downloaded : ", wcount)
            wcount = wcount + 1
    except FileNotFoundError as err:  # If something Wrong with Local Path
        print(err)
    except HTTPError as err:  # IF something Wrong with HTTP Downloading
        print(err)


def ChangeWallpaper():
    # wcount = 0
    while True:
        SPI_SETDESKWALLPAPER = 20
        try:
            lis = WallpaperAddress()
            list_Length = len(lis)
            wcount = random.randint(0, list_Length - 1)
            print(wcount)
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpapercount(wcount), 0)
            print("**********************Wallpaper Changed********************")
            # wcount = wcount + 1
            time.sleep(900)
        except FileNotFoundError as err:
            print(err)


def wallpapercount(wcount):
    # wcount = wcount + 1
    return ("C:/Users/_ansh_/Desktop/wallpapers/" + str(wcount) + ".jpg")


def WallpaperAddress():
    user_url = input("Enter URl : ")
    if (user_url == ""):
        url = "http://www.santabanta.com/wallpapers/categories/0/?order=popular"
    else:
        url = user_url
        # url=urllib.request.urlopen("http://www.santabanta.com/wallpapers/indian-celebrities(f)/2/")
    url = urllib.request.urlopen(url)
    soup = BeautifulSoup(url, "html.parser")
    lst = []
    for link in soup.find_all('a'):
        if link.has_attr('href'):
            if '/photos' in link['href']:
                # print(link['href'])
                # print(type(link))
                lst.append(link['href'])
    print("***************Returning URLs List****************")
    return lst


def fetchPhotos(url):
    # print(url)
    url = urllib.request.urlopen(url)
    # print(url)
    soup = BeautifulSoup(url, "html.parser")
    url = soup.find_all('img', {"src": re.compile('http://media1.santabanta.com/full1.*')})
    # print(url)
    for i in url:
        print("**************Sending Individual Photo URL**************")
        return (i.get('src'))
    # print(type(url))


def deleteExisting():
    try:
        shutil.rmtree("C:/Users/_ansh_/Desktop/wallpapers/")
        print("*********************Existing Wallpaper Folder Deleted*******************************")
        time.sleep(2)
    except OSError:
        pass


def createFolder():
    directory = "C:/Users/_ansh_/Desktop/wallpapers/"
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print("*********************New Wallpaper Folder Created****************")
            time.sleep(2)
        except OSError as e:
            if e.errorno != errorno.EEXIST:
                raise


deleteExisting()
createFolder()
downloadImage()
ChangeWallpaper()