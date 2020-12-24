import re
import time
import pandas as pd
import numpy as np
import constants
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import NoSuchElementException

def scrapLeaderboard():
	with webdriver.Firefox() as driver:
		driver.get("http://www.dota2.com/leaderboards#americas-0")
		wait = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, "leaderboard_body"))
		#unpredictable results with WebDriverWait, so we force wait
		time.sleep(3)
		leaderboard = driver.find_element(By.ID, "leaderboard_body")
		rows = leaderboard.find_elements(By.TAG_NAME, "tr")
		data = []
		rank = 0
		errors = 0
		#variables to track progress
		perc25 = len(rows)/4
		prog_dic = dict([(int(perc25 * idx), str((perc25 * idx * 100) // len(rows)) + " percent") for idx in range(1,5)])
		for idx, row in enumerate(rows, start=1):
			rank += 1
			name = "" 
			clan = ""
			sponsor = ""
			country_iso = ""
			flag_link = ""
			try:
				name = row.find_element(By.CSS_SELECTOR, ".player_name").text
			except:
				errors += 1
			try:
				clan = row.find_element(By.CSS_SELECTOR, ".team_tag").text
			except:
				pass
			try:
				sponsor = row.find_element(By.CSS_SELECTOR, ".sponsor").text
			except:
				pass
			try:
				flag_link = row.find_element(By.TAG_NAME, "img").get_attribute("src")
				match = re.search(r"\w+(?=\.\w+$)", flag_link)
				if match:
					country_iso = match.group()
			except:
				pass
			
			data.append([rank, name, clan, sponsor, country_iso, flag_link])
			#show progress
			if idx in prog_dic:
				print("scrapping...", prog_dic[idx], "done")

		print("scrapping input errros:", errors)

	return data

def saveLeaderBoard(data):
	df = pd.DataFrame(data)
	df.columns = ["rank", "name", "clan", "sponsor", "country iso", "flag link"]
	file_name = constants.LEADERBOARD_FILE
	df.to_csv("generated/" + file_name, index=False)
	print("wrote to", file_name)
	return df

def countCountries(df_data):
	counter = {}
	for idx, entry in df_data.iterrows():
		key = entry["country iso"]
		if key:
			#good idea forcing it to be lower for further comparisons
			key = key.lower()
		else:
			key = constants.NO_COUNTRY_KEY

		if key in counter:
			counter[key] += 1
		else:
			counter[key] = 1

	counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)
	return dict(counter)

def saveCountryStats(count_dict):
	iso_dict = {}
	with open("generated/" + constants.COUNTRY_ISO_FILE, "r", encoding="utf8") as iso_file:
		lines = iso_file.read().split("\n")
		regex = re.compile(r"(\w+)[\,.]+([\w\W]+)$")
		#Ignoring the first line, because it's a header
		for line in lines[1:]:
			try:
				match = regex.search(line)
				code = match.groups()[0].lower()
				country = match.groups()[1]
				iso_dict[code] = country
			except Exception as e:
				print("invalid line", line, "exception", e)

	#write full country names with stats to file
	file_name = constants.COUNTRY_STATS_FILE
	with open("generated/" + file_name, "w", encoding="utf8") as file:
		file.write("country,total\n")
		for code in count_dict:
			if code in iso_dict:
				file.write(iso_dict[code] + "," + str(count_dict[code]) + "\n")
			else:
				print("warning country " + code + " not found!")
				file.write(code + "," + str(count_dict[code]) + "\n")
		print("wrote to", file_name)


#---Main---
data = scrapLeaderboard()
df = saveLeaderBoard(data)
count_dict = countCountries(df)
saveCountryStats(count_dict)


