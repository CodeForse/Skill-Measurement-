from re import sub

import pydantic
import requests
import numpy as np
from bs4 import BeautifulSoup 
from selenium.webdriver import Chrome
from selenium import webdriver
from time import sleep

# main problem - define how to define id or in general players into sample

# https://destinytracker.com/destiny-2/profile/steam/4611686018490833395/overview
# https://warmind.io/analytics/item/emblems?page=3
# +bungie.net 
# will be used to create dataset
def getNumbersInt(soup: BeautifulSoup):
    try:
        return int(sub("[^0-9]","",str(soup.text)))
    except: return 0

urlDT_overview="https://destinytracker.com/destiny-2/profile/steam/4611686018490833395/overview"
request_overview=requests.get(urlDT_overview)
soup_overview= BeautifulSoup(request_overview.text,'lxml')

# nickname=soup_overview.find('span',class_='trn-ign__username').text.strip('\n')
# nickname=nickname[:nickname.find('\n')].strip()

# numViews=soup_overview.find('div',class_='ph-details__subtitle').find_all('span')[1]

# numViews=getNumbersInt(numViews)  #damn optimization 

# id_bungie=soup_overview.find('div','ph-details__identifier').find('span','ph-details__name').find('span','trn-ign__discriminator')
# id_bungie=getNumbersInt(id_bungie)

# urlDT_detailed="https://destinytracker.com/destiny-2/profile/steam/4611686018490833395/detailed?mode=AllPvP"
# request_detailed=requests.get(urlDT_overview)
# soup_detailed= BeautifulSoup(request_detailed.text,'lxml')

# kd_overall=float(soup_overview.find('div','segment-stats regular-stats card bordered header-bordered responsive').find('div','stat align-left expandable').find('span','value').text)

# hoursPlayed=soup_overview.find('div','segment-stats').findAll('span','matches')[1]
# hoursPlayed=getNumbersInt(hoursPlayed)

# favor_weapon=soup_overview.find('div',class_='weapons-list').find('div',class_='name').text
# print(favor_weapon) #most used last 30 
class Player(pydantic.BaseModel):
    prime_steam_id: str
    nick_name: str
    id_bungie: int
    views: int
    kd_overall: float
    win_rate: float
    hours_played: int
    show_offName: bool


    # def setPlayer(self,steam_id:str):
    #     urlDT_overview=f"https://destinytracker.com/destiny-2/profile/steam/{steam_id}/overview"
    #     request_overview=requests.get(urlDT_overview)
    #     soup_overview= BeautifulSoup(request_overview.text,'lxml')

    #     self.prime_steam_id=steam_id

    #     nickname=soup_overview.find('span',class_='trn-ign__username').text.strip('\n')
    #     self.nickname=nickname[:nickname.find('\n')].strip()

    #     numViews=soup_overview.find('div',class_='ph-details__subtitle').find_all('span')[1]
    #     self.numViews=getNumbersInt(numViews)  #damn optimization 

    #     id_bungie=soup_overview.find('div','ph-details__identifier').find('span','ph-details__name').find('span','trn-ign__discriminator')
    #     self.id_bungie=getNumbersInt(id_bungie)

    #     self.kd_overall=float(soup_overview.find('div','segment-stats regular-stats card bordered header-bordered responsive').find('div','stat align-left expandable').find('span','value').text)
    #     self.win_rate=getNumbersInt(soup_overview.find('div','segment-stats regular-stats card bordered header-bordered responsive').findAll('div','stat align-left expandable')[2].find('span','value').text)

    #     hoursPlayed=soup_overview.find('div','segment-stats').findAll('span','matches')[1]
    #     self.hours_played=getNumbersInt(hoursPlayed)

    #sl=(index)3.5% adjusted rarity to compare with, the idea is to get dummy variable - emblem is rare or not
def getEmblemRarity(steam_id:str,SL:float):
    urlBungie='https://www.bungie.net/en/Profile/GameHistory/3/'+steam_id
    soupBungie=BeautifulSoup(requests.get(urlBungie).text,'lxml') 

    emblem=str(soupBungie.find('div','select-option js-option-selectable').find('div','icon'))
    emblem='https://bungie.net'+emblem[48:len(emblem)-10]
    
    #warmind part, percentage is different from stated in https://bray.tech/
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver=Chrome(executable_path='C:/Users/User/Downloads/chromedriver_win32/chromedriver.exe',options=options)
    
    page=3
    while(page>0):
        urlWarmind=f'https://warmind.io/analytics/item/emblems?page{page}'
        page-=1
        driver.get(urlWarmind)
        sleep(1500)
        rarity=driver.find_element_by_class_name(name='panel-body')
        print(rarity)
        # soupWarmind=BeautifulSoup(requests.get(urlWarmind).text,'lxml')
        # try:
        #     rarity=soupWarmind.find('div','col-xs-12').find('div','panel-body')
        #     print(rarity)
        # except:
        #     print('not found')
        #     continue
    driver.close()
        
        
        




def setPlayer(steam_id:str):
        urlDT_overview=f"https://destinytracker.com/destiny-2/profile/steam/{steam_id}/overview"
        request_overview=requests.get(urlDT_overview)
        soup_overview= BeautifulSoup(request_overview.text,'lxml')

        prime_steam_id=steam_id

        nickname=soup_overview.find('span',class_='trn-ign__username').text.strip('\n')
        nickname=nickname[:nickname.find('\n')].strip()

        numViews=soup_overview.find('div',class_='ph-details__subtitle').find_all('span')[1]
        numViews=getNumbersInt(numViews)  #damn optimization 

        id_bungie=soup_overview.find('div','ph-details__identifier').find('span','ph-details__name').find('span','trn-ign__discriminator')
        id_bungie=getNumbersInt(id_bungie)

        kd_overall=float(soup_overview.find('div','segment-stats regular-stats card bordered header-bordered responsive').find('div','stat align-left expandable').find('span','value').text)
        win_rate=float(soup_overview.find('div','segment-stats regular-stats card bordered header-bordered responsive').findAll('div','stat align-left expandable')[2].find('span','value').text.replace('%',''))

        hoursPlayed=soup_overview.find('div','segment-stats').findAll('span','matches')[1]
        hoursPlayed=getNumbersInt(hoursPlayed)

        show_off= bool(nickname.__len__()<=6) #defining show-off guy is a guestion to ML, here i define it as just short nickname

        player=Player(prime_steam_id=prime_steam_id,nick_name=nickname,id_bungie=id_bungie,views=numViews,kd_overall=kd_overall, win_rate=win_rate,hours_played=hoursPlayed, show_offName=show_off)
        return(player)

getEmblemRarity('4611686018490833395',3.5)

# try:
#     file=open('players.json','a')
# except:
#     file=open('players.json','w')
    
# file.write(setPlayer('4611686018493562197').json()+',\n')

# file.close()


