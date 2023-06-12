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

driver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=driver_service)
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# ARGUMENTS
link = "https://www.wunderground.com/history"
# link = "https://www.youtube.com/watch?v=yKVcDu7vv4w&ab_channel=SpaceX"
# link = "https://www.youtube.com/watch?v=vcsSc2iksC0"
# link = "https://www.youtube.com/watch?v=Hb5ZXUeGPHc&t=3s"
# DateRange = str(sys.argv[2])
# driver.get(link)
# driver.implicitly_wait(2)

with open("zip_codes.txt") as f:
    zip_codes = f.readlines()
    new_zip_list = []
    for i in range(len(zip_codes)):
        if zip_codes[i] != "\n":
            if i != len(zip_codes) - 1:
                new_zip_list.append(zip_codes[i][:len(zip_codes[i]) - 1])
            else:
                new_zip_list.append(zip_codes[i][:len(zip_codes[i])])

    new_zip_list = new_zip_list[171:]
    print(new_zip_list)
    for zip in new_zip_list:
        try:
            driver.get(link)
            driver.implicitly_wait(2)    
            # zip = "63011"
            # zip = "63960"
            input = zip + " Missouri"
            input_field = driver.find_element(By.XPATH, '//*[@id="historySearch"]').send_keys(input)
            sleep(1)

            first_option = driver.find_element(By.XPATH, '//*[@id="historyForm"]/search-autocomplete/ul/li[2]')
            sleep(1)
            print(first_option.text)
            first_option.click()
            sleep(1)
            view_btn = driver.find_element(By.XPATH, '//*[@id="dateSubmit"]').click()
            sleep(6)
            station = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[1]/lib-city-header/div[1]/div/div/a[1]')
            print(station.get_attribute("href"))
            driver.get(station.get_attribute("href"))
            sleep(6)

            if len(driver.find_elements(By.XPATH, '//*[@id="inner-content"]/div[1]/app-dashboard-header/div[2]/div/div[2]/div/lib-pws-info-icon/mat-icon')) != 0:
                station_info = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[1]/app-dashboard-header/div[2]/div/div[2]/div/lib-pws-info-icon/mat-icon').click()
                sleep(1)
                station_id = driver.find_element(By.XPATH, '//*[@id="mat-dialog-0"]/lib-about-pws/mat-dialog-content/div/div/strong/span')
                station_id = station_id.text
                sleep(1)
                lat_long_info = driver.find_element(By.XPATH, '//*[@id="mat-dialog-0"]/lib-about-pws/mat-dialog-content/div/div/p[2]/span[1]')
                lat_long_info = str(lat_long_info.text)

                lat, long = lat_long_info.split(',')
                lat = lat[:6]
                long = "-" + long[1:7]
                
                zip_to_latlong_id = open("zip_codes$latlong$id.txt", "a")
                zip_to_latlong_id.write(str(zip) + "$" + lat + ", " + long + "$" + str(station_id) + "\n")
                zip_to_latlong_id.close()
            else:
                zip_to_latlong_id = open("zip_codes$latlong$id.txt", "a")
                zip_to_latlong_id.write(str(zip) + "$" + "NA" + "$" + "NA" + "\n")
                zip_to_latlong_id.close()

            sleep(6)
        except:
            zip_to_latlong_id = open("zip_codes$latlong$id.txt", "a")
            zip_to_latlong_id.write(str(zip) + ": " + "Exception occured.\n")
            zip_to_latlong_id.close()
            continue
