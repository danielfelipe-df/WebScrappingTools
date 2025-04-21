"""
@file examples/NGA/download_image_from_url.py
@date 2025-04-21
@author Daniel Felipe <danielfoc@protonmail.com>

@brief Main program to download an image and metadata form National Gallery of ART (NGA).

This program save the information in a CSV located in the same folder where the image is saved
"""


import os
import time
import pandas as pd
from selenium.webdriver.common.by import By

import src.browser_web_scrapping as browser_ws


# Variables
nga_image_url = "https://www.nga.gov/collection/art-object-page.43626.html"

# Create browser driver and set download folder
download_path = os.path.join(os.getcwd(), 'dat')
if not os.path.exists(download_path):
	os.makedirs(download_path)
driver = browser_ws.create_browser_connection(download_path)

# Display Image URL in the browser
driver = browser_ws.login_to_url(driver, nga_image_url)
time.sleep(5)

# Set the list with all XPATH with util information
xpath_atributes_list = [
	"//div[@class='object-attr medium']",
	"//div[@class='object-attr dimensions']",
	"//div[@class='object-attr credit']",
	"//div[@class='object-attr accession']",
	"//div[@class='object-attr artists-makers']"
]

# Save informaion from XPATHs in Dictionary Form
data_dict = {'Attribute': [], 'Value': []}
for xpath in xpath_atributes_list:
	element = browser_ws.find_element_in_driver(driver, By.XPATH, xpath)
	info_list = element.text.split('\n', maxsplit=1)
	data_dict['Attribute'].append(info_list[0])
	data_dict['Value'].append(info_list[1])

# Get description and save it in the Dictionary
xpath_button = "//button[@id='drawer-control-0']"
button_element = browser_ws.find_element_in_driver(driver, By.XPATH, xpath_button)
if browser_ws.click_element_in_driver(button_element, need_scroll=True, driver=driver):
	time.sleep(1)
	xpath_description = "//div[@id='drawer-content-0']"
	description_element = browser_ws.find_element_in_driver(driver, By.XPATH, xpath_description)
	data_dict['Attribute'].append('Description')
	data_dict['Value'].append(description_element.text)

# Find element to download image
xpath_download = "//a[@title='download image']"
download_button = browser_ws.find_element_in_driver(driver, By.XPATH, xpath_download)
image_url = download_button.get_attribute('href')
image_name = image_url.split('=')[-1]
if browser_ws.click_element_in_driver(download_button, need_scroll=True, driver=driver):
	print("Image successfully downloaded")
else:
	print("Image NOT successfully downloaded")

# Create DataFrame from Dictionary and save it as CSV
df = pd.DataFrame(data_dict)
df.insert(0, 'ImageURL', [image_url]*len(df))
df.insert(0, 'InfoURL', [nga_image_url]*len(df))
df.insert(0, 'ImageName', [image_name]*len(df))
df.insert(0, 'ID', [nga_image_url.split('.')[-2]]*len(df))
df.to_csv(f"{download_path}/data.csv", sep="|", index=False, encoding="utf-8")

driver.quit()
