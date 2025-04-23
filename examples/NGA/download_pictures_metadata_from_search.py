"""
@file examples/NGA/download_pictures_metadata_from_search.py
@date 2025-04-23
@author Daniel Felipe <danielfoc@protonmail.com>

@brief Main program to download URL metadata form National Gallery of ART (NGA).

This program save the information in a CSV located in the same folder where the image is saved
"""


import os
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import  ActionChains

import src.browser_web_scrapping as browser_ws


# Variables
nga_search_url = "https://www.nga.gov/collection-search-result.html?classification=painting"

# Create browser driver and set download folder
download_path = os.path.join(os.getcwd(), 'dat')
if not os.path.exists(download_path):
	os.makedirs(download_path)
driver = browser_ws.create_browser_connection(download_path)

# Display Image URL in the browser
driver = browser_ws.login_to_url(driver, nga_search_url)
time.sleep(5)

# Get ImageID and link to it
links = []
images = []
pages = []
position = []
while True:
	print(driver.current_url)

	# Get all links in the classes of tag 'a' because they have the links
	links_dirty = driver.find_elements(By.TAG_NAME, "a")

	# Save the links and related info
	count = 0
	for element_link in links_dirty:
		link = element_link.get_attribute("href")		
		if 'art-object-page' in link:
			image_id = link.split('.')[-2]
			if image_id not in images:
				links.append(link)
				images.append(image_id)
				pages.append(driver.current_url)
				position.append(count)
				count += 1

	# Locate the mouse at (0, 0) and locate the button to next page
	browser_ws.locate_cursor_in_position(driver)
	next_elements = driver.find_elements(By.CLASS_NAME, "results-next")
	time.sleep(3)

	# If there were found elements, then get that unique element and click to appear in the next page
	if len(next_elements) > 0:
		new_page = next_elements[0].get_attribute("href")
		browser_ws.click_element_in_driver(next_elements[0], need_scroll=True, driver=driver)
		time.sleep(3)

		browser_ws.locate_cursor_in_position(driver)
		time.sleep(1)
	else:
		break

# Create DataFrame from Dictionary and save it as CSV
df = pd.DataFrame({'ImageID': images, 'ImageLink': links, 'PagePosition': position, 'PageLink': pages})
df.to_csv(f"{download_path}/data_pages.csv", sep="|", index=False, encoding="utf-8")

driver.quit()
