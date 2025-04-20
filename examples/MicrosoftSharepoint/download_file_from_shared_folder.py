"""
@file examples/MicrosoftSharepoint/download_file_from_shared_folder.py
@date 2025-04-19
@author Daniel Felipe <danielfoc@protonmail.com>

@brief Main program to download a file from a shared folder in Microsoft Sharepoint
"""


import os
import time
from selenium.webdriver.common.by import By

import src.browser_web_scrapping as browser_ws


# Variables
sharepoint_folder_url = "https://basename.sharepoint.com/OtherUser/FolderName"
file_name = "NameOfFile.ext"

# Create browser driver and set download folder
download_path = os.path.join(os.getcwd(), 'dat')
if not os.path.exists(download_path):
	os.makedirs(download_path)
driver = browser_ws.create_browser_connection(download_path)

# Display URL Folder in the browser
driver = browser_ws.login_to_url(driver, sharepoint_folder_url)
time.sleep(3)

# Find row of the file to download
xpath_div_file = f"//button[text()='{file_name}']/ancestor::div[@role='row']"
div_file = browser_ws.find_element_in_driver(driver, By.XPATH, xpath_div_file)

# Click the div to select the complete row
is_downloaded = False
if browser_ws.click_element_in_driver(div_file):
	time.sleep(1)

	# Right click on the row to show the file options
	if browser_ws.context_click_element_in_driver(driver, div_file):
		time.sleep(1)

		# Find the download element displayed
		xpath_download_button = "//button[@data-automationid='downloadCommand' and @aria-disabled='false']"
		download_button = browser_ws.find_element_in_driver(driver, By.XPATH, xpath_download_button)

		# Click the download button of the file
		if browser_ws.click_element_in_driver(download_button):
			print(f"Successful download of file '{file_name}' from shared folder")
			is_downloaded = True

if not is_downloaded:
	print(f"An error occurred downloading file '{file_name}' from shared folder")

driver.quit()
