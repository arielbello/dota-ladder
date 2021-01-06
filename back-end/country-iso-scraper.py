import constants
import utils
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

def getCountryIsoData():
	'''
	Scrapes "https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2" for country
	codes and respective names

	@return: country codes and full names in a Panda.DataFrame
	'''
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
		return df

def saveDataFrameToCSV(df, path):
	utils.create_folder_if_needed(constants.GENERATED_FOLDER)
	df.to_csv(path, index=False, encoding="utf-8")
	print("wrote to", path)

def main():
	df = getCountryIsoData()
	path = constants.GENERATED_FOLDER + "/" + constants.COUNTRY_ISO_CSV
	saveDataFrameToCSV(df, path)

if __name__ == "__main__":
	main()