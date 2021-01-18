import constants as Const
import utils
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


def _get_data():
    """
	Scrapes "https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2" for country
	codes and respective names

	@return: country codes and full names in a Panda.DataFrame
	"""
    # headless usage
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver_options.add_argument("--disable-extensions")
    with webdriver.Firefox(options=driver_options) as driver:
        # Countries 2 letter iso wikipedia page
        driver.get(Const.Urls.COUNTRY_ISO)
        try:
            WebDriverWait(driver, 10).until(lambda d: d.find_element(By.CSS_SELECTOR, "table.wikitable.sortable"))
        except TimeoutException:
            print("Time exceeded, ", TimeoutException)
        # unpredictable results with WebDriverWait, so we force wait
        time.sleep(4)
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


def _save_dataframe_to_csv(df, path):
    utils.create_folder_if_needed(Const.Files.GENERATED)
    df.to_csv(path, index=False, encoding="utf-8")
    print("wrote to", path)


def scrape():
    df = _get_data()
    path = Const.Files.GENERATED + "/" + Const.Files.COUNTRY_ISO
    _save_dataframe_to_csv(df, path)
