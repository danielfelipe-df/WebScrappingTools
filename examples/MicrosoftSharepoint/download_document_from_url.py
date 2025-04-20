"""
@file examples/MicrosoftSharepoint/download_document_from_url.py
@date 2025-04-19
@author Daniel Felipe <danielfoc@protonmail.com>

@brief Main program to download a file in Microsoft Sharepoint.

At the moment it only support Word Documents saved in Sharepoint, and can be downloaded in DOCX or PDF format
"""


import os
import time
from selenium.webdriver.common.by import By

import src.browser_web_scrapping as browser_ws


# Variables
file_url = "https://basename.sharepoint.com/FolderName/NameOfFile.ext&OtherKindOfTokens"
file_name = "NameOfFile.ext"
format = 'PDF'

# Create browser driver and set download folder
download_path = os.path.join(os.getcwd(), 'dat')
if not os.path.exists(download_path):
	os.makedirs(download_path)
driver = browser_ws.create_browser_connection(download_path)

# Depending on the format set the variables for the flow
if format == 'WORD':
	flow_dict = {
		'side_panel': "//span[text()='Create a Copy']",
		'download': "//span[text()='Download a copy']",
		'confirm': "//span[text()='Download a copy']"
	}
elif format == 'PDF':
	flow_dict = {
		'side_panel': "//span[text()='Export']",
		'download': "//span[text()='Download as PDF']",
		'confirm': "//span[text()='Download']"
	}
else:
	raise ValueError(f"Format '{format}' invalid in download document from URL. Allowed formats are {allowed_formats}")

# Display URL Folder in the browser
driver = browser_ws.login_to_url(driver, file_url)
time.sleep(3)

# Detect the iframe related to the Word document for do the Scrapping
xpath_iframe_document = "//iframe[@id='WacFrame_Word_0']"
iframe_document = browser_ws.find_element_in_driver(driver, By.XPATH, xpath_iframe_document)

# Switch to the Word iframe
is_downloaded = False
if browser_ws.switch_to_frame_in_browser(driver, iframe_document):

	# Find the element to display 'File' options
	xpath_document_button = "//button[@id='FileMenuFlyoutLauncher']"
	document_button = browser_ws.find_element_in_driver(driver, By.XPATH, xpath_document_button)

	# Click on the 'File' options
	if browser_ws.click_element_in_driver(document_button):
		time.sleep(1)

		# Find the element of the frist element to download the file
		xpath_side_panel_button = flow_dict['side_panel']
		side_panel_button = browser_ws.find_element_in_driver(driver, By.XPATH, xpath_side_panel_button)

		# Click this first element to download the file
		if browser_ws.click_element_in_driver(side_panel_button):
			time.sleep(1)

			# Find the download button element
			xpath_download_button = flow_dict['download']
			download_button = browser_ws.find_element_in_driver(driver, By.XPATH, xpath_download_button)

			# Click on the download button
			if browser_ws.click_element_in_driver(download_button):
				time.sleep(5)

				# Find the element to confirm the download
				xpath_confirm_button = flow_dict['confirm']
				confirm_button = browser_ws.find_element_in_driver(driver, By.XPATH, xpath_confirm_button)

				# Click the confirmation button
				if browser_ws.click_element_in_driver(confirm_button):
					print(f"Successful download of file '{file_name}' from url")
					is_downloaded = True

if not is_downloaded:
	print(f"An error occurred downloading file '{file_name}' from url")

driver.quit()
