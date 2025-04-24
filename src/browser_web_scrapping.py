"""
@file src/browser_web_scrapping.py
@date 2025-04-19
@author Daniel Felipe <danielfoc@protonmail.com>

@brief Useful functions to interact with the browser for Web Scrapping
"""


import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import chrome, firefox, Chrome, Firefox
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager



def create_browser_connection(download_folder: str, browser: str = 'Firefox', pref_dict: dict = None) -> Chrome | Firefox:
	"""
	Creates a Selenium WebDriver instance for Chrome with custom download settings.

	@param download_folder The path to the folder where downloads should be saved.
	@param browser The name of the browser will be used.
	@param pref_dict The dictionary of preferences needed to setup the browser.
	@return A Selenium WebDriver instance.
	"""

	# Check the browser is one of the options supported
	avaliable_browsers = ['Chrome', 'Firefox']
	if browser not in avaliable_browsers:
		raise ValueError(f"Browser '{browser}' not in available browsers {avaliable_browsers}")

	# Default dictionary of preferences
	default_pref_dict = {
		'Chrome': {
			'download.default_directory': download_folder,
			'download.prompt_for_download': False,
			'safebrowsing.enabled': True
		},
		'Firefox': {
			'browser.download.folderList': 2,
			'browser.download.manager.showWhenStarting': False,
			'browser.download.dir': download_folder,
			'browser.helperApps.neverAsk.saveToDisk': 'application/octet-stream'
		}
	}

	# If the preferences dictionary from the arguments is None, use the default
	pref_dict = default_pref_dict[browser] if pref_dict is None else pref_dict

	try:
		if browser == 'Chrome':
			options = chrome.options.Options()
			options.add_experimental_option("prefs", pref_dict)
			options.add_argument("--start-maximized")

			service = chrome.service.Service(ChromeDriverManager().install())
			driver = Chrome(service=service, options=options)

		else:
			options = firefox.options.Options()
			for preference, value in pref_dict.items():
				options.set_preference(preference, value)
			options.add_argument("--start-maximized")

			service = firefox.service.Service(GeckoDriverManager().install())
			driver = Firefox(service=service, options=options)

		return driver
	except Exception as e:
		raise Exception(f"An error occurred creating the browser connection: {e}")


def login_to_url(driver: webdriver.Chrome, url: str, needs_credentials: bool = False) -> webdriver.Chrome:
	"""
	Opens a browser window to a specified URL and waits for manual login.

	@param driver A Selenium WebDriver instance.
	@param url The URL to navigate to for login.
	@param needs_credentials Boolean to permit input credentials if needed
	@return The WebDriver instance after manual login.
	"""

	try:
		driver.get(url)

		if needs_credentials:
			print("Log in manually and press Enter here...")
			input()

		return driver
	except Exception as e:
		driver.quit()
		raise Exception(f"An error occurred logging in browser: {e}")



def find_element_in_driver(driver: webdriver.Chrome, type_element: By, element: str, verbose: bool = False) -> WebElement:
	"""
	Finds an element in a Selenium WebDriver instance using the specified locator type.

	@param driver A Selenium WebDriver instance.
	@param type_element The type of locator (e.g., By.ID, By.CLASS_NAME, By.XPATH).
	@param element The element selector string.
	@param verbose Whether to print the outer HTML of the found element, defaults to False.
	@return The found web element.
	"""

	try:
		element_found = driver.find_element(type_element, element)

		if verbose:
			print(element_found.get_attribute("outerHTML"))

		return element_found
	except Exception as e:
		print(f"An error occurred finding element: {e}")
		return None


def click_element_in_driver(element: WebElement, need_scroll: bool = False, driver = None) -> bool:
	"""
	Clicks on a web element using Selenium WebDriver.

	@param element The web element to be clicked.
	@param need_scroll Boolean which move (scroll) the driver to the element.
	@param driver The driver of the current session, mandatory if scrolling need to be done.
	@return True if the click is successful, False otherwise.
	"""

	if need_scroll:
		if driver is None:
			raise ValueError(f"If scroll is needed then driver is required")
		else:
			driver.execute_script("arguments[0].scrollIntoView(true);", element)
			time.sleep(2)

	try:
		element.click()
		return True

	except Exception as e:
		print(f"An error occurred clicking element: {e}")
		return False


def context_click_element_in_driver(driver: webdriver.Chrome, element: WebElement) -> bool:
	"""
	Performs a right-click (context click) on a web element using Selenium WebDriver.

	@param driver The Selenium WebDriver instance.
	@param element The web element to be right-clicked.
	@return True if the context click is successful, False otherwise.
	"""

	try:
		action = ActionChains(driver)
		action.context_click(element).perform()
		return True

	except Exception as e:
		print(f"An error occurred doing context click in element: {e}")
		return False


def switch_to_frame_in_browser(driver: webdriver.Chrome, frame) -> bool:
  """
  Switches to a specified iframe in the browser using Selenium WebDriver.

  @param driver The Selenium WebDriver instance.
  @param frame The frame element or frame name/index to switch to.
  @return True if the switch is successful, False otherwise.
  """

  try:
    driver.switch_to.frame(frame)
    return True

  except Exception as e:
    print(f"An error occurred switching to frame: {e}")
    return False


def return_from_frame_in_browser(driver: webdriver.Chrome) -> bool:
	"""
	Switches back to the main content from an iframe using Selenium WebDriver.

	@param driver The Selenium WebDriver instance.
	@return True if the switch is successful, False otherwise.
	"""

	try:
		driver.switch_to.default_content()
		return True

	except Exception as e:
		print(f"An error occurred returning from frame: {e}")
		return False


def locate_cursor_in_position(driver: webdriver.Chrome, x: str|int = 'min', y: str|int = 'min'):
	"""
	Move the cursor to a specific position on the page..

	:param driver: Chrome WebDriver instance
	:param x: X-coordinate or 'min'/'max' for minimum/maximum scroll width
	:param y: Y-coordinate or 'min'/'max' for minimum/maximum scroll height
	:return: None
	"""

	availabe_categories = ['min', 'max']
	if not (x in availabe_categories or y in availabe_categories or isinstance(x, int) or isinstance(y, int)):
		raise ValueError(f"{x} and {y} are not valid in the cursor location function.")

	if x in availabe_categories:
		x = 0 if x == 'min' else 'document.body.scrollWidth'
	
	if y in availabe_categories:
		y = 0 if y == 'min' else 'document.body.scrollHeight'

	try:
		driver.execute_script(f"window.scrollTo({x}, {y});")
	except Exception as e:
		raise Exception(f"An error occurred locating the cursor in position: {e}")
