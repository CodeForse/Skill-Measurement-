
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
person_json=json.loads(BeautifulSoup(driver.page_source).text)['data']
bungie_name= person_json['platformInfo']['platformUserHandle']
steam_id=person_json['platformInfo']['platformUserIdentifier']
num_views=person_json['userInfo']['pageViews']
country_code=person_json['userInfo']['countryCode']
isSuspicious_by_Tracker=person_json['userInfo']['isSuspicious']
plays_Trials=person_json['metadata']['playsTrials']
playing_Trials=person_json['metadata']['playingTrials']

#total info

#site_score
site_score_rank=person_json['stats']['siteScore']['rank']
site_score_percentile=person_json['stats']['siteScore']['percentile']
site_score_value=person_json['stats']['siteScore']['value']

#ability_kills
ability_kills_rank=person_json['stats']['abilityKills']['rank']
ability_kills_percentile=person_json['stats']['abilityKills']['percentile']
ability_kills_value=person_json['stats']['abilityKills']['value']

#assists
assists_rank=person_json['stats']['assists']['rank']
assists_percentile=person_json['stats']['assists']['percentile']
assists_value=person_json['stats']['assists']['value']

#assists_pga
assists_pga_rank=person_json['stats']['assistsPga']['rank']
assists_pga_percentile=person_json['stats']['assistsPga']['percentile']
assists_pga_value=person_json['stats']['assistsPga']['value']

#total_kill_distance [metres i quess]
total_kill_distance_rank=person_json['stats']['totalKillDistance']['rank']
total_kill_distance_percentile=person_json['stats']['totalKillDistance']['percentile']
atotal_kill_distance_value=person_json['stats']['totalKillDistance']['value']

#kills
kills_rank=person_json['stats']['kills']['rank']
kills_percentile=person_json['stats']['kills']['percentile']
kills_value=person_json['stats']['kills']['value']

#kills_pga
kills_pga_rank=person_json['stats']['killsPga']['rank']
kills_pga_percentile=person_json['stats']['killsPga']['percentile']
kills_pga_value=person_json['stats']['killsPga']['value']

#average_kill_distance #bagged?
average_kill_distance_rank=person_json['stats']['avgKillDistance']['rank']
average_kill_distance_percentile=person_json['stats']['avgKillDistance']['percentile']
average_kill_distance_value=person_json['stats']['avgKillDistance']['value']

#seconds_played #yes they really calc seconds and then converty into hours
seconds_played_rank=person_json['stats']['secondsPlayed']['rank']
seconds_played_percentile=person_json['stats']['secondsPlayed']['percentile']
seconds_played_value=person_json['stats']['secondsPlayed']['value']

#deaths
deaths_rank=person_json['stats']['deaths']['rank']
deaths_percentile=person_json['stats']['deaths']['percentile']
deaths_value=person_json['stats']['deaths']['value']

#average_life_span  seems to be empty and not available for user
average_life_span_rank=person_json['stats']['averageLifeSpan']['rank']
average_life_span_percentile=person_json['stats']['averageLifeSpan']['percentile']
average_life_span_value=person_json['stats']['averageLifeSpan']['value']

#score ???
score_rank=person_json['stats']['score']['rank']
score_percentile=person_json['stats']['score']['percentile']
score_value=person_json['stats']['score']['value']

#score_pga
score_pga_rank=person_json['stats']['scorePga']['rank']
score_pga_percentile=person_json['stats']['scorePga']['percentile']
score_pga_value=person_json['stats']['scorePga']['value']

#average_score_per_kill
average_score_per_kill_rank=person_json['stats']['avgScorePerKill']['rank']
average_score_per_kill_percentile=person_json['stats']['avgScorePerKill']['percentile']
average_score_per_kill_value=person_json['stats']['avgScorePerKill']['value']

#average_score_per_life
average_score_per_life_rank=person_json['stats']['avgScorePerLife']['rank']
average_score_per_life_percentile=person_json['stats']['avgScorePerLife']['percentile']
average_score_per_life_value=person_json['stats']['avgScorePerLife']['value']

#best_single_game_kills
best_single_game_kills_rank=person_json['stats']['bestSingleGameKills']['rank']
best_single_game_kills_percentile=person_json['stats']['bestSingleGameKills']['percentile']
best_single_game_kills_value=person_json['stats']['bestSingleGameKills']['value']

#best_single_game_score
best_single_game_score_rank=person_json['stats']['bestSingleGameScore']['rank']
best_single_game_score_percentile=person_json['stats']['bestSingleGameScore']['percentile']
best_single_game_score_value=person_json['stats']['bestSingleGameScore']['value']

#domination_kills
domination_kills_rank=person_json['stats']['dominationKills']['rank']
domination_kills_percentile=person_json['stats']['dominationKills']['percentile']
domination_kills_value=person_json['stats']['dominationKills']['value']

#kd
kd_rank=person_json['stats']['kd']['rank']
kd_percentile=person_json['stats']['kd']['percentile']
kd_value=person_json['stats']['kd']['value']

#kad
kad_rank=person_json['stats']['kad']['rank']
kad_percentile=person_json['stats']['kad']['percentile']
kad_value=person_json['stats']['kad']['value']

#objectives_completed : don't know what the data is about
objectives_completed_rank=person_json['stats']['objectivesCompleted']['rank']
objectives_completed_percentile=person_json['stats']['objectivesCompleted']['percentile']
objectives_completed_value=person_json['stats']['objectivesCompleted']['value']

#suicides 
suicides_rank=person_json['stats']['suicides']['rank']
suicides_percentile=person_json['stats']['suicides']['percentile']
suicides_value=person_json['stats']['suicides']['value']

#win_ratio
win_ratio_rank=person_json['stats']['wl']['rank']
win_ratio_percentile=person_json['stats']['wl']['percentile']
win_ratio_value=person_json['stats']['wl']['value']

#longest_

driver.close()

# soup=BeautifulSoup(driver.page_source,'lxml')
# page_code=''
# for elem in soup.find_all('span','cm-comment'):
#     print(elem.text)
# print(page_code,1)


# driver.close()
