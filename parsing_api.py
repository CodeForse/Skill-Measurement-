
from re import sub
from typing import List
import json

import pydantic
import requests
import numpy as np
from bs4 import BeautifulSoup 
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

from urllib.request import urlopen
import nltk
from fake_useragent import UserAgent
# main problem - define how to define id or in general players into sample

# https://destinytracker.com/destiny-2/profile/steam/4611686018490833395/overview
# https://warmind.io/analytics/item/emblems?page=3
# +bungie.net 
# will be used to create dataset

#now we have full acess to hiden api: https://api.tracker.gg/api/v2/destiny-2/standard/profile/steam/4611686018490833395
# matches https://api.tracker.gg/api/v2/destiny-2/standard/profile/steam/4611686018490833395/sessions?perspective=pvp
#don't know for what https://api.tracker.gg/api/v2/destiny-2/standard/profile/steam/4611686018490833395?__cf_chl_tk=QAKGMsZrZIuP7J1UvHlYFP6FI1cGKOwl2DIIO3Nx8.8-1657895171-0-gaNycGzNBz0

ua = UserAgent()

headers={'User-Agent':str(ua.chrome)}
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
url_tracker_api='https://api.tracker.gg/api/v2/destiny-2/standard/profile/steam/4611686018490833395?__cf_chl_tk=QAKGMsZrZIuP7J1UvHlYFP6FI1cGKOwl2DIIO3Nx8.8-1657895171-0-gaNycGzNBz0'
#url_tracker_api='https://api.tracker.gg/api/v2/destiny-2/standard/profile/steam/4611686018490833395'
# request_tracker=requests.get(url_tracker_api,headers=headers)


# print(request_tracker.content)

#error 403 acces deny

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("start-maximized")        
driver=Chrome(service=Service(ChromeDriverManager().install()),options=options)

driver.get(url_tracker_api)

sleep(5)

driver.close()

# soup=BeautifulSoup(driver.page_source,'lxml')
# page_code=''
# for elem in soup.find_all('span','cm-comment'):
#     print(elem.text)
# print(page_code,1)


# driver.close()