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

# Options for running headless (No GUI). Can be commented out to run with GUI.
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

def weather_scraper(start_idx, end_idx, out_file):
    '''
    Wunderground gives two slightly different interfaces depending on the type of station that is selected. This scraper deals with "PWS"
    stations. leftover_stations.py then finds leftover "general" stations for weather_scraper_general(1).py to scrape.
    Written to be parallelized.
    
    start_idx, end_idx: The respective indices of stations in all_stations.txt to scrape.
    out_file: The output file to write scraped station info to.
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
        
        if len(driver.find_elements(By.XPATH, '//*[@id="inner-content"]/div[2]/lib-city-header/div[2]/lib-subnav/div/div[3]/ul/li[5]/a')) > 0:
            station_indices.remove(station)
            continue
        else:
            success = False
            for attempt in range(3):
                try:
                    monthly_mode = driver.find_element(By.XPATH, '//*[@id="modeSelect"]/option[3]').click()
                    sleep(5)


                    weather_dict = {}
                    for i in range(4):
                        year_select = driver.find_element(By.XPATH, '//*[@id="yearSelect"]')
                        years = year_select.find_elements(By.TAG_NAME, 'option')
                        year_str = years[i + 1].text

                        year_select.click()
                        years[i + 1].click()
                        print(years[i + 1].text)
                        sleep(1)

                        for j in range(12):
                            month_select = driver.find_element(By.XPATH, '//*[@id="monthSelect"]')
                            months = month_select.find_elements(By.TAG_NAME, 'option')
                            month_str = months[j].text
                            months[j].click()
                            print(month_str)
                            sleep(1)

                            view_btn = driver.find_element(By.XPATH, '//*[@id="main-page-content"]/div/div/div/lib-history/div[1]/div[2]/button').click()
                            sleep(6)

                            table_btn = driver.find_element(By.XPATH, '//*[@id="history-tab-group"]/li[2]/a').click()
                            sleep(3)

                            weather_table = driver.find_element(By.XPATH, '//*[@id="main-page-content"]/div/div/div/lib-history/div[2]/lib-history-table/div/div/div/table/tbody')
                            rows = weather_table.find_elements(By.TAG_NAME, 'tr')

                            for row in rows:
                                weather_values = row.find_elements(By.TAG_NAME, 'td')
                                date = weather_values[0].text

                                value = ""
                                for idx in range(1, len(weather_values)):
                                    if idx == len(weather_values) - 1:
                                        value += weather_values[idx].text
                                    elif idx % 3 == 0:
                                        value += weather_values[idx].text + "/"
                                    else:
                                        value += weather_values[idx].text + "-"
                                weather_dict[date] = value

                            # print(weather_dict)
                    weather_stations_list.append(weather_dict)
                    success = True
                    break
                except Exception as exc:
                    print(exc)
                    sleep(10)
                    driver.refresh()
                    sleep(30)

            if success != True:
                station_indices.remove(station)
                continue
    

    df = pandas.DataFrame(weather_stations_list, index=station_indices)
    df = df.to_csv(out_file, index = True)


weather_scraper(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])