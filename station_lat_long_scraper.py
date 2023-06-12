import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import sqlite3
import sys
import pandas

driver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=driver_service)

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
# options.add_argument("--disable-software-rasterizer")
options.add_argument("--ignore-certificate-errors-spki-list")
options.add_argument("--ignore-ssl-errors")
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=options)

# ARGUMENTS
link = "https://www.wunderground.com"

def station_scraper(start_idx, end_idx, out_file):
    '''
    Scrapes lat/long info for each station in all_stations.txt. Written to be parallelized.
    
    start_idx, end_idx: The respective indices of stations in all_stations.txt to scrape.
    out_file: The output file to write scraped lat/long info to.
    '''
    station_list = []

    with open("all_stations.txt") as f:
        stations = f.readlines()
        
        for i in range(len(stations)):
            if stations[i] != "\n":
                if i != len(stations) - 1:
                    station_list.append(stations[i][:len(stations[i]) - 1])
                else:
                    station_list.append(stations[i][:len(stations[i])])

        station_list = station_list[start_idx:end_idx]
        print(station_list)

    station_indices = station_list.copy()
    weather_stations_list = []
    for station in station_list:
        success = False
        for i in range(3):
            try:
                driver.get(link)
                driver.implicitly_wait(5)    

                input_field = driver.find_element(By.XPATH, '//*[@id="wuSearch"]').send_keys(station)
                sleep(3)

                first_option = driver.find_element(By.XPATH, '//*[@id="wuForm"]/search-autocomplete/ul/li[2]/a/span[1]')
                sleep(3)
                print(first_option.text)

                first_option.click()
                sleep(3)

                sleep(10)
                success = True
                break
            except Exception as exc:
                sleep(10)
                print(exc)
                driver.refresh()
                sleep(20)

        
        if success != True:
            station_indices.remove(station)
            continue
        
        if len(driver.find_elements(By.XPATH, '//*[@id="inner-content"]/div[1]/app-dashboard-header/div[2]/div/div[1]/span')) > 0:
            lat_long = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[1]/app-dashboard-header/div[2]/div/div[1]/span')
            lat_long = lat_long.text
            print(lat_long)
            elev_lat_long = lat_long.split(",")
            lat = elev_lat_long[1][1:len(elev_lat_long[1])]
            long = elev_lat_long[2][1:len(elev_lat_long[2])]
            file = open(out_file, "a")
            file.write(station + ";" + lat + ";" + long + "\n")
            file.close()
            # print(lat)
            # print(long)
        elif len(driver.find_elements(By.XPATH, '//*[@id="inner-content"]/div[2]/lib-city-header/div[1]/div/span')) > 0:
            lat_long = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[2]/lib-city-header/div[1]/div/span')
            lat_long = lat_long.text
            print(lat_long)
            lat, long = lat_long.split(",")
            long = long[1:len(long)]
            file = open(out_file, "a")
            file.write(station + ";" + lat + ";" + long + "\n")
            file.close()
            # print(lat)
            # print(long)
        else:
            station_indices.remove(station)
            continue


# station_scraper(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])

def find_missing_station_info():
    '''
    Find the stations that had missing lat/long info during scraping
    '''
    stations_1 = []
    with open("station_lat_long1.txt", "r") as f1:
        stations_1 = f1.readlines()

    stations_2 = []
    with open("station_lat_long_2.txt", "r") as f2:
        stations_2 = f2.readlines()

    stations = stations_1 + stations_2
    print(len(stations))

    all_stations = []
    with open("all_stations.txt") as f:
        all_stations = f.readlines()

    all_stations_2 = []
    for station in all_stations:
        # all_stations_2.append(station)
        found = False
        for s in stations:
            s, lat, long = s.split(";")
            s = s + "\n"
            if s == station:
                found = True
        if not found:
            print(station)

    # print(all_stations[1:15])
    # print(all_stations_2[1:15])

# find_missing_station_info()

def combine_station_lists():
    '''
    Stations were scraped from all_stations.txt using two separate processes. This function combines them into one .txt file
    '''
    stations_1 = []
    with open("station_lat_long1.txt", "r") as f1:
        stations_1 = f1.readlines()

    stations_2 = []
    with open("station_lat_long_2.txt", "r") as f2:
        stations_2 = f2.readlines()

    with open("stations_lat_long.txt", "a") as f:
        for s in stations_1:
            f.write(s)
        for s in stations_2:
            f.write(s)

# combine_station_lists()