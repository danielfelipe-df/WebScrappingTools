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


df = pd.read_csv("dat/data_pages.csv", delimiter="|", encoding="utf-8")

# Variables
nga_image_url = "https://www.nga.gov/collection/art-object-page.43626.html"

# Create browser driver and set download folder
download_path = os.path.join(os.getcwd(), 'dat/')
if not os.path.exists(download_path):
	os.makedirs(download_path)
driver = browser_ws.create_browser_connection(download_path)

df_headers = pd.DataFrame(columns=['ID', 'ImageName', 'InfoURL', 'ImageURL', 'Attribute', 'Value'])
df_headers.to_csv(f"{download_path}/data.csv", sep="|", index=False, encoding="utf-8")
#df_in = pd.read_csv(f"{download_path}/data.csv", delimiter="|", encoding="utf-8")
#df = df[~df['ImageID'].isin(df_in['ID'])]

# Set the list with all XPATH with util information
xpath_atributes_list = [
	"//div[@class='object-attr medium']",
	"//div[@class='object-attr dimensions']",
	"//div[@class='object-attr credit']",
	"//div[@class='object-attr accession']",
	"//div[@class='object-attr artists-makers']"
]


count = 0
for nga_image_url in df['ImageLink']:
	nga_image_url = nga_image_url.replace("/content/ngaweb", "")
	print(f"{nga_image_url} is the image {count} of {len(df)}")

	# Display Image URL in the browser
	driver = browser_ws.login_to_url(driver, nga_image_url)
	time.sleep(5)

	# Get the collection name if found, otherwise set as empty string
	collection = ""
	try:
		info_element = browser_ws.find_element_in_driver(driver, By.XPATH, "//div[@id='oe-strip-wrap']")
		collection = info_element.text.replace('\n', '')
	except Exception as e:
		print("Can't be found the element")

	# Save informaion from XPATHs in Dictionary Form
	data_dict = {'Attribute': ['Collection'], 'Value': [collection]}
	for xpath in xpath_atributes_list:
		element = browser_ws.find_element_in_driver(driver, By.XPATH, xpath)
		if element is not None:
			info_list = element.text.split('\n', maxsplit=1)
			data_dict['Attribute'].append(info_list[0])
			data_dict['Value'].append(info_list[1])
		else:
			print(f"In {xpath} the element gotten is None")

	# Get description and save it in the Dictionary
	xpath_button = "//button[@id='drawer-control-0']"
	button_element = browser_ws.find_element_in_driver(driver, By.XPATH, xpath_button)
	if button_element is not None:
		if browser_ws.click_element_in_driver(button_element, need_scroll=True, driver=driver):
			time.sleep(1)
			xpath_description = "//div[@id='drawer-content-0']"
			description_element = browser_ws.find_element_in_driver(driver, By.XPATH, xpath_description)
			data_dict['Attribute'].append('Description')
			data_dict['Value'].append(description_element.text)
		else:
			print(f"Click in the button {xpath_button} was False")
	else:
		print(f"In {xpath_button} the element gotten is None")

	# Find element to download image
	xpath_download = "//a[@title='download image']"
	download_button = browser_ws.find_element_in_driver(driver, By.XPATH, xpath_download)
	image_name = ""
	image_url = ""
	if download_button is not None:
		image_url = download_button.get_attribute('href')
		image_name = image_url.split('=')[-1]
		if browser_ws.click_element_in_driver(download_button, need_scroll=True, driver=driver):
			print("Image successfully downloaded")
		else:
			print("Image NOT successfully downloaded")
	else:
		print(f"In {xpath_download} the element gotten is None")

	# Get Analysis (Entry Tab) and save it in the Dictionary
	xpath_button = "//button[@id='tab-entry']"
	button_element = browser_ws.find_element_in_driver(driver, By.XPATH, xpath_button)
	if button_element is not None:
		if browser_ws.click_element_in_driver(button_element, need_scroll=True, driver=driver):
			time.sleep(1)
			xpath_description = "//div[@data-id='entry']"
			description_element = browser_ws.find_element_in_driver(driver, By.XPATH, xpath_description)
			data_dict['Attribute'].append('Entry')
			data_dict['Value'].append(description_element.text)
		else:
			print(f"Click in the button {xpath_button} was False")
	else:
		print(f"In {xpath_button} the element gotten is None")

	# Create DataFrame from Dictionary and save it as CSV
	df = pd.DataFrame(data_dict)
	df.insert(0, 'ImageURL', [image_url]*len(df))
	df.insert(0, 'InfoURL', [nga_image_url]*len(df))
	df.insert(0, 'ImageName', [image_name]*len(df))
	df.insert(0, 'ID', [nga_image_url.split('.')[-2]]*len(df))
	df.to_csv(f"{download_path}/data.csv", sep="|", index=False, encoding="utf-8", mode="a", header=False)
	time.sleep(5)

	count += 1

driver.quit()
