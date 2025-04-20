"""
@file examples/MicrosoftSharepoint/download_folder.py
@date 2025-04-19
@author Daniel Felipe <danielfoc@protonmail.com>

@brief Main program to download folder from Microsoft Sharepoint
"""


import os
import time
from selenium.webdriver.common.by import By

import src.browser_web_scrapping as browser_ws


# Variables
sharepoint_url = "https://basename.sharepoint.com"
folder_name = "MySharepointFolderRelativePath"
folder_url = f"{sharepoint_url}/{folder_name}"

# Create browser driver and set download folder
download_path = os.path.join(os.getcwd(), 'dat')
if not os.path.exists(download_path):
	os.makedirs(download_path)
driver = browser_ws.create_browser_connection(download_path)

# Display URL Folder in the browser
driver = browser_ws.login_to_url(driver, folder_url)
time.sleep(3)

# Find Download Folder button element
xpath_download_button = "//button[@data-automationid='downloadCommand']"
download_button = browser_ws.find_element_in_driver(driver, By.XPATH, xpath_download_button)
time.sleep(1)

# Click the button to download folder
if browser_ws.click_element_in_driver(download_button):
	print(f"Successful download of folder '{folder_name}'")
else:
	print(f"An error occurred downloading folder '{folder_name}'")

driver.quit()
