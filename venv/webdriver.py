
####################################################
if __name__ == '__main__':
	print("\nRunning '%s'." %(__file__))
else:
	print("Importing '%s'." %(__file__))
####################################################
#
import time
"""
Ensure that selenium is imported. If not, go to:
Default settings => project interpreter; add selenium as a package.
"""
from selenium import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#
import os
folder_path = os.path.dirname(os.path.abspath(__file__))
driver_path = folder_path + "/chromedriver"
print(driver_path)

class driver(webdriver.Chrome):
	"""
	Usage:
	* Start a driver:
	=> d = driver(url)
	=> d = driver(url, headless=False)
	- the latter if you want to see the webpage when scraped - recommended for developing.

	* Methods for finding web-element:
		* For specific elements such as buttons, use Xpath (copy full Xpath from 'inspect element'):
		=> x_path = >>someting like "/html/div/XXX/jgjgkj/jsksg"<<
		=> element = d.find_element_by_xpath(x_path)
	* Methods for finding web-elementS - in plural:
		* Use identifiers that match the items you want to find, such as "tr" or "td".
		=> list_of_elements = d.find_elements_by_tag_name("tr")
	* Using the elements:
		* I have mostly been using the text-data which is can be obtain by the .text suffix.
		=> element_text = element.text
		or for lists
		=> for element in list_of_elements:
				element_text = element.text
	"""
	all_drivers = list()
	options = webdriver.ChromeOptions()
	chrome_prefs = {}
	options.experimental_options["prefs"] = chrome_prefs
	chrome_prefs["profile.default_content_settings"] = {"images": 2}
	def __init__(self, path=driver_path, headless = True):
		driver.all_drivers.append(self)
		self.options = driver.options
		if headless == True:
			self.options.add_argument("--headless")  
		webdriver.Chrome.__init__(self, path, chrome_options=self.options)
	def open_new_tab(self, url):
		self.execute_script("window.open('"+str(url)+"');")
		return self.window_handles[-1] #Tab window_handle
	def wait_until_element_is_loaded(self, xpath, timeout = 10, method=By.XPATH):
		element = WebDriverWait(self, timeout).until(EC.presence_of_element_located((method, xpath)))
		return element

def quit_all():
	for d in driver.all_drivers:
		for handle in d.window_handles:
			d.switch_to.window(handle)
			d.close()
		d.quit()

if __name__ == "__main__":
	d = driver(headless=False)
	d.get("https://www.google.com")
	d.quit()