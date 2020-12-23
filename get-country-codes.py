import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

with webdriver.Firefox() as driver:
	#Countries 2 letter iso wikipedia page
	driver.get("https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2")
	wait = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.CSS_SELECTOR, "table.wikitable.sortable"))
	#unpredictable results with WebDriverWait, so we force wait
	time.sleep(3)
	table = driver.find_element(By.CSS_SELECTOR, "table.wikitable.sortable")
	table_body = table.find_element(By.TAG_NAME, "tbody")
	rows = table_body.find_elements(By.TAG_NAME, "tr")
	country_list = []

	for row in rows:
		data = row.find_elements(By.TAG_NAME, "td")
		entry = [data[0].text, data[1].text]
		country_list.append(entry)

	df = pd.DataFrame(country_list)
	df.columns = ['code', 'name']
	file_name = "country_iso.csv"
	df.to_csv('generated/'+ file_name, index=False, encoding="utf-8")
	print("wrote to", file_name)
