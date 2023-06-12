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

driver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=driver_service)

# Options for running headless (No GUI). Can be commented out to run with GUI.
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
# options.add_argument("--disable-software-rasterizer")
options.add_argument("--ignore-certificate-errors-spki-list")
options.add_argument("--ignore-ssl-errors")
driver = webdriver.Chrome(options=options)

# ARGUMENTS
link = "https://www.wunderground.com/history"

def stations_scraper(start_idx, end_idx, out_file):
    '''
    Wunderground provides a list of nearby weather stations when selecting a weather station. This scraper goes through every zip code in MO,
    and clicks the first option provided by Wunderground for that zip code. It then collects all nearby weather stations to that station. 
    Written to be parallelized.
    
    start_idx, end_idx: The respective indices of zip in zip_codes.txt to scrape.
    out_file: The output file to write scraped station info to.
    '''
    with open("zip_codes.txt") as f:
        zip_codes = f.readlines()
        new_zip_list = []
        for i in range(len(zip_codes)):
            if zip_codes[i] != "\n":
                if i != len(zip_codes) - 1:
                    new_zip_list.append(zip_codes[i][:len(zip_codes[i]) - 1])
                else:
                    new_zip_list.append(zip_codes[i][:len(zip_codes[i])])

        new_zip_list = new_zip_list[start_idx:end_idx]
        print(new_zip_list)

        for zip in new_zip_list:
            # try:
            driver.get(link)
            driver.implicitly_wait(5)    
            # zip = "63011"
            # zip = "63960"
            input = zip + " Missouri"
            input_field = driver.find_element(By.XPATH, '//*[@id="historySearch"]').send_keys(input)
            sleep(3)

            first_option = driver.find_element(By.XPATH, '//*[@id="historyForm"]/search-autocomplete/ul/li[2]')
            sleep(3)
            print(first_option.text)
            first_option.click()
            sleep(3)

            while True:
                try:
                    view_btn = driver.find_element(By.XPATH, '//*[@id="dateSubmit"]').click()
                    sleep(8)

                    change_btn = driver.find_element(By.XPATH, '//*[@id="station-select-button"]').click()
                    sleep(8)

                    nearby_stations_list = driver.find_element(By.XPATH, '//*[@id="stationselector_table"]')
                    # nearby_stations_list = nearby_stations_list.find_element(By.XPATH, '//*[@id="stationselector_table"]')
                    # print(nearby_stations_list)
                    nearby_stations = nearby_stations_list.find_elements(By.CLASS_NAME, 'stationselectorRowPWS')
                    # print(len(nearby_stations))
                    for station in nearby_stations:
                        # station = driver.find_element(By.TAG_NAME, 'a')
                        # print(1)
                        prefix, suffix = str(station.text).split("(")
                        station_id = suffix[:len(suffix) - 1]
                        file = open(out_file, "a")
                        file.write(station_id + "\n")
                        file.close()
                        # print(station.text)
                    break
                except:
                    sleep(30)
                    driver.refresh()
                    sleep(10)


stations_scraper(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])