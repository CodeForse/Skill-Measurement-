
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


class Player(pydantic.BaseModel):
    prime_steam_id: str
    nick_name: str
    id_bungie: int
    views: int
    kd_overall: float
    win_rate: float
    hours_played: int
    show_offName: bool


    

#sl=(index)3.5% adjusted rarity to compare with, the idea is to get dummy variable - emblem is rare or not
def getEmblemRarity(steam_id:str,SignLevel:float): #takes to much time so i prefer write new method to scrap for the whole sample at once
    urlBungie='https://www.bungie.net/en/Profile/GameHistory/3/'+steam_id
    soupBungie=BeautifulSoup(requests.get(urlBungie).text,'lxml') 

    emblem=str(soupBungie.find('div','select-option js-option-selectable').find('div','icon'))
    emblem='https://bungie.net'+emblem[48:len(emblem)-10]
    
    #warmind part, percentage is different from stated in https://bray.tech/
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("start-maximized")
    #driver=Chrome(executable_path='D:/Users/Аслан/Desktop/программирование/PythonDanila/chromedriver.exe',options=options)
    driver=Chrome(service=Service(ChromeDriverManager().install()),options=options)
    page=4
    urlWarmind=f'https://warmind.io/analytics/item/emblems?page={page}'
    driver.get(urlWarmind)
    while(page>0):
        
        
        
        sleep(5)
        
        
            # rarity=driver.find_element(By.XPATH,"//img[@src='https://www.bungie.net/common/destiny2_content/icons/7e4ad40ea82544394255424482f2f490.jpg']")
            #print(rarity)
            
            # print(driver.find_element(By.CLASS_NAME,'col-lg-2').find_element(By.))
        soup=BeautifulSoup(driver.page_source,'lxml')

        #here i'll use adjusted value of rarity that is in general bigger than global rarity, so it will be easier to compare rares
        #to track global rariry just change col-lg-6 to col-lg-5
        try:
            rarity=soup.find(attrs={'src':emblem}).parent.find('div','col-lg-6').find('span').text
            rarity=float(rarity[:-1])
            return rarity<=SignLevel # 0 - not rare; 1 - rare 
                   
        except: pass
        
        
        if(page>1):
            driver.find_element(By.LINK_TEXT,'Previous Page').click() #optimization by logic
        
        page-=1
    
    driver.close()          
    return False #suppose that all new emblems(that are not in the site) are not rare (0)

class emblem(pydantic.BaseModel):
    src: str
    rarity: float
class emblemList(pydantic.BaseModel):
    emblems: List[emblem]
def getAllEmblems():
    if(True):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("start-maximized")        
        driver=Chrome(service=Service(ChromeDriverManager().install()),options=options)  
        page=4 #last page may change over a time
        urlWarmind=f'https://warmind.io/analytics/item/emblems?page={page}'
        driver.get(urlWarmind)
        

        list_emblems=[]
        while(page>0):
            sleep(5)
            soup=BeautifulSoup(driver.page_source,'lxml')
            #make a table and then findall?
            imgs=soup.find_all('img')
            for img in imgs:
                
                if(img.has_attr('id') and img.get('id')!='modal-image'):
                    src=img.get('src')
                    #here i'll use adjusted value of rarity that is in general bigger than global rarity, so it will be easier to compare rares
                    #to track global rariry just change col-lg-6 to col-lg-5
                    rarity=float(img.parent.find('div','col-lg-6').find('span').text[:-1])
                    list_emblems.append(emblem(src= src,rarity= rarity))

            if(page>1):
                driver.find_element(By.LINK_TEXT,'Previous Page').click() #optimization by logic
            page-=1
        
        

        driver.close()  

        file=open('emblems.json','w')
        file.write(emblemList(emblems=list_emblems).json())
        file.close()

               
def getEmblemRarity_sampleBased(sample:List[Player]):
    try:
        emblem_file=open('emblems.json','r')  
    except: #if warmind was updated with new emblems - just delete the current file [no user interface, but maybe i'll make it]
        getAllEmblems()
        emblem_file=open('emblems.json','r')

    emblems=emblem_file.read()   




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

        return Player(prime_steam_id=prime_steam_id,nick_name=nickname,id_bungie=id_bungie,views=numViews,kd_overall=kd_overall, win_rate=win_rate,hours_played=hoursPlayed, show_offName=show_off)
        
    
# print(getEmblemRarity('4611686018493562197',3.5)) 
#getAllEmblems()

# try:
#     file=open('players.json','a')
# except:
#     file=open('players.json','w')
    
# file.write(setPlayer('4611686018493562197').json()+',\n')

# file.close()


