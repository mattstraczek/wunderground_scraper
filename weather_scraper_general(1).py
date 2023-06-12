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
driver = webdriver.Chrome(options=options)

# ARGUMENTS
link = "https://www.wunderground.com/history"

def weather_scraper(start_idx, end_idx, out_file):
    '''
    Wunderground gives two slightly different interfaces depending on the type of station that is selected. This scraper deals with "general"
    stations that are leftover after weather_scraper_PWS(2).py scrapes the "PWS" stations.
    Written to be parallelized.
    
    start_idx, end_idx: The respective indices of stations in leftover_stations.txt to scrape.
    out_file: The output file to write scraped station info to.
    '''
    
    station_list = []

    with open("leftover_stations.txt") as f:
        stations = f.readlines()
        
        for i in range(len(stations)):
            station_list.append(stations[i][:len(stations[i]) - 1])

        station_list = station_list[start_idx:end_idx]
        print(station_list)

    station_indices = station_list.copy()
    weather_stations_list = []
    for station in station_list:
        # try:
        success = False
        for i in range(3):
            try:
                driver.get(link)
                driver.implicitly_wait(5)    

                input_field = driver.find_element(By.XPATH, '//*[@id="historySearch"]').send_keys(station)
                sleep(3)

                first_option = driver.find_element(By.XPATH, '//*[@id="historyForm"]/search-autocomplete/ul/li[2]')
                sleep(3)
                print(first_option.text)

                first_option.click()
                sleep(3)

                view_btn = driver.find_element(By.XPATH, '//*[@id="dateSubmit"]').click()
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
        
        success = False
        for attempt in range(3):
            try:
                monthly_mode = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[2]/div[1]/div[1]/div[1]/div/lib-link-selector/div/div/div/a[3]').click()
                sleep(5)

                weather_dict = {}
                for i in range(4):
                    year_select = driver.find_element(By.XPATH, '//*[@id="yearSelection"]')
                    years = year_select.find_elements(By.TAG_NAME, 'option')
                    year_str = years[i + 1].text

                    year_select.click()
                    years[i + 1].click()
                    print(years[i + 1].text)
                    sleep(1)
                    

                    for j in range(12):
                        month_select = driver.find_element(By.XPATH, '//*[@id="monthSelection"]')
                        months = month_select.find_elements(By.TAG_NAME, 'option')
                        month_str = months[j].text
                        months[j].click()
                        sleep(1)

                        view_btn = driver.find_element(By.XPATH, '//*[@id="dateSubmit"]').click()
                        sleep(6)

                        date_column = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table/tbody/tr/td[1]/table')
                        dates = date_column.find_elements(By.TAG_NAME, 'tr')

                        temp_column = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table/tbody/tr/td[2]/table')
                        temps = temp_column.find_elements(By.TAG_NAME, 'tr')

                        dew_pt_column = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table/tbody/tr/td[3]/table')
                        dew_pts = dew_pt_column.find_elements(By.TAG_NAME, 'tr')

                        humidity_column = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table/tbody/tr/td[4]/table')
                        humidities = humidity_column.find_elements(By.TAG_NAME, 'tr')

                        wind_speed_column = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table/tbody/tr/td[5]/table')
                        wind_speeds = wind_speed_column.find_elements(By.TAG_NAME, 'tr')

                        pressure_column = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table/tbody/tr/td[6]/table')
                        pressures = pressure_column.find_elements(By.TAG_NAME, 'tr')

                        precipitation_column = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table/tbody/tr/td[7]/table')
                        precipitations = precipitation_column.find_elements(By.TAG_NAME, 'tr')

                        for d in range(len(dates)):
                            if d != 0:
                                max_temp, avg_temp, min_temp = temps[d].find_elements(By.TAG_NAME, 'td')
                                max_dew_pt, avg_dew_pt, min_dew_pt = dew_pts[d].find_elements(By.TAG_NAME, 'td')
                                max_humidity, avg_humidity, min_humidity = humidities[d].find_elements(By.TAG_NAME, 'td')
                                max_wind_speed, avg_wind_speed, min_wind_speed = wind_speeds[d].find_elements(By.TAG_NAME, 'td')
                                max_pressure, avg_pressure, min_pressure = pressures[d].find_elements(By.TAG_NAME, 'td')
                                precipitation = precipitations[d]

                                data_string = max_temp.text + "-" + avg_temp.text + "-" + min_temp.text + "/" + max_dew_pt.text + "-" + avg_dew_pt.text + "-" + min_dew_pt.text + "/" + max_humidity.text + "-" + avg_humidity.text + "-" + min_humidity.text + "/" + max_wind_speed.text + "-" + avg_wind_speed.text + "-" + min_wind_speed.text + "/" + max_pressure.text + "-" + avg_pressure.text + "-" + min_pressure.text + "/" + precipitation.text
                                weather_dict[month_str + "-" + dates[d].text + "-" + year_str] = data_string

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