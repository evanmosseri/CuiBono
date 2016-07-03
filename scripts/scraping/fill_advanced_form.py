from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import seleniumrequests
from selenium.webdriver.support.ui import Select
from datetime import datetime
from time import strftime
from scripts.scraping.scrape_politican import get_filer_info
from scripts.utils import PrintException

from time import time, sleep

driver = seleniumrequests.Chrome()

try:
	driver.get("https://www.ethics.state.tx.us/Jasper/AdvancedSearch.html")

	transaction_type = Select(driver.find_element_by_name("transaction"))
	transaction_type.select_by_visible_text("Contributions")

	search_type = Select(driver.find_element_by_name("searchtype"))
	search_type.select_by_visible_text("By Filer ID")

	datetype = Select(driver.find_element_by_name("datetype"))
	datetype.select_by_visible_text("By Specific Date Range")

	begin_date = driver.find_element_by_name("begin_date")
	begin_date.send_keys("2000-01-01")

	end_date = driver.find_element_by_name("end_date")
	# end_date.send_keys(strftime("%Y-%m-%d"))
	end_date.send_keys(strftime("2015-05-01"))

	filer_info = get_filer_info("kirk","watson")[0]

	filer_id = driver.find_element_by_name("iactno")
	filer_id.send_keys(filer_info["id"])

	filer_type_selection = driver.find_element_by_name("Filertype")
	filer_type = Select(filer_type_selection)
	print(filer_info["type"])
	print([x.get_attribute("value") for x in filer_type_selection.find_elements_by_tag_name("option")])

	filer_type.select_by_value(filer_info["type"])

	driver.find_element_by_name("format2").submit()

	WebDriverWait(driver,1000).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".jrPage")))
	driver.implicitly_wait(10)
	sleep(5)
	driver.find_element_by_id("button").click()

	driver.implicitly_wait(10)
	sleep(200)

	driver.close()
except Exception as e:
	PrintException()
	driver.close()



