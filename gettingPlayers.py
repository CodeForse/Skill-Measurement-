

from ctypes import LittleEndianStructure
import random
import pydantic
import requests
import numpy as np
from bs4 import BeautifulSoup 
import time
from selenium.webdriver import Chrome
import selenium.webdriver
import re
# urlDT_nullPlayer="https://destinytracker.com/destiny-2/profile/steam/4611686018490833395/overview"
# request_overview=requests.get(urlDT_nullPlayer)
# soup_overview= BeautifulSoup(request_overview.text,'lxml')

#Random.randint(3*10**len(46116860184908332),5*10**len(46116860184908332)) bullshit
# idPlayer="46116860184908332"
# url=f"https://destinytracker.com/destiny-2/profile/steam/{idPlayer}/overview"
# request=requests.get(url)
# soup=BeautifulSoup(request.text,'lxml')
# try:
#     print(soup.find('span',class_='trn-ign__username').text)
# except:
#         print('not exist')

# options=selenium.webdriver.ChromeOptions()
# options.headless=True
# # options.add_argument('--ignore-certificate-errors')
# # options.add_argument('--ignore-ssl-errors')

# driver=Chrome(executable_path='C:/Users/User/Downloads/chromedriver_win32/chromedriver.exe')#,options=options)
# driver.get('https://destinytracker.com/destiny-2/profile/steam/4611686018490833395/overview')
# time.sleep(3000)
#matches=driver.find_elements_by_class_name('match-row')
#print(matches)

# buttons=driver.find_element_by_class_name('trn-gamereport-list__group-entries').find_elements_by_tag_name('input')
# print(buttons)
# buttons[0].click()
# time.sleep(3000)
# game_results=driver.find_element_by_class_name('match-rosters')
# print(game_results.text)

# favor_weapon=driver.find_element_by_class_name('weapons-list-item').find_element_by_class_name('name').text
# print(favor_weapon)

# games=driver.find_elements_by_class_name('match-row match-row--won')
# buttonTemp=games[0].find_element_by_class_name('match-row__expand')
# print(buttonTemp)

##https://destinytracker.com/destiny-2/leaderboards/seasonal/all/elo?playlist=84&seasonStats=elo&type=seasonal&page=200
#new easy way to obtain dataset, scale by elo

# driver.quit()


def writeAllPlayers(page:int):
    url=f'https://destinytracker.com/destiny-2/leaderboards/seasonal/steam/elo?playlist=84&seasonStats=elo&type=seasonal&page={page}'
    request=requests.get(url)
    soup=BeautifulSoup(request.text,'lxml')
    
    primeKey_SteamFile=open('primeKeyID.txt','w')
    for link in soup.find_all('a'):
     if('destiny-2/profile' in str(link.get('href'))):
            id=str(link.get('href'))[len('/destiny-2/profile/steam/'):]
            primeKey_SteamFile.write(id+'\n')
            
    
    primeKey_SteamFile.close()
    
    

