import constants
import utils
import re
import time
import pandas as pd
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import NoSuchElementException


def scrapLeaderboard():
    # headless usage
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver_options.add_argument("--disable-extensions")
    driver = webdriver.Firefox(options=driver_options)

    driver.get("http://www.dota2.com/leaderboards#americas-0")
    WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, "leaderboard_body"))
    # unpredictable results with WebDriverWait, so we force wait
    time.sleep(3)
    soup = BS(driver.page_source, "lxml")
    driver.close()
    rows = soup.find(id="leaderboard_body").find_all("tr")
    data = []
    rank = 0
    errors = 0
    # variables to track progress
    perc25 = len(rows) / 4
    prog_dic = dict([(int(perc25 * idx), str((perc25 * idx * 100) // len(rows)) + "%") for idx in range(1, 5)])
    for idx, row in enumerate(rows, start=1):
        rank += 1
        name = ""
        clan = ""
        sponsor = ""
        country_iso = ""
        flag_link = ""
        try:
            name = row.find(class_="player_name").get_text()
        except:
            errors += 1
        try:
            clan = row.find(class_="team_tag").get_text()
        except:
            pass
        try:
            sponsor = row.find(class_="sponsor").get_text()
        except:
            pass
        try:
            flag_link = row.find("img")["src"]
            match = re.search(r"\w+(?=\.\w+$)", flag_link)
            if match:
                country_iso = match.group()
        except:
            pass

        data.append([rank, name, clan, sponsor, country_iso, flag_link])
        # show progress
        if idx in prog_dic:
            print("scrapping...", prog_dic[idx], "done")

    print("scrapping input errros:", errors)

    return data


def writeLeaderboardToCSV(data):
    df = pd.DataFrame(data)
    df.columns = ["rank", "name", "clan", "sponsor", "country iso", "flag link"]
    file_name = constants.LEADERBOARD_FILE
    utils.create_folder_if_needed(constants.GENERATED_FOLDER)
    path = constants.GENERATED_FOLDER + "/" + file_name
    df.to_csv(path, index=False)
    print("wrote to", path)
    return df


def countCountries(df_data):
    counter = {}
    for idx, entry in df_data.iterrows():
        key = entry["country iso"]
        if key:
            # good idea forcing it to be lower for further comparisons
            key = key.lower()
        else:
            key = constants.NO_COUNTRY_KEY

        if key in counter:
            counter[key] += 1
        else:
            counter[key] = 1

    counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    return dict(counter)


def writeCountryStatsCSV(count_dict):
    iso_dict = {}
    path = constants.GENERATED_FOLDER + "/" + constants.COUNTRY_ISO_CSV
    with open(path, "r", encoding="utf8") as iso_file:
        lines = iso_file.read().split("\n")
        regex = re.compile(r"(\w+)[\,.]+([\w\W]+)$")
        # Ignoring the first line, because it's a header
        for line in lines[1:]:
            if not line.strip():
                continue
            try:
                match = regex.search(line)
                code = match.groups()[0].lower()
                country = match.groups()[1]
                iso_dict[code] = country
            except Exception as e:
                print("invalid line", line, "exception", e)

    # write full country names with stats to file
    utils.create_folder_if_needed(constants.GENERATED_FOLDER)
    path = constants.GENERATED_FOLDER + "/" + constants.COUNTRY_STATS_CSV
    with open(path, "w", encoding="utf8") as file:
        file.write("country,total\n")
        for code in count_dict:
            if code in iso_dict:
                file.write(iso_dict[code] + "," + str(count_dict[code]) + "\n")
            else:
                file.write(code + "," + str(count_dict[code]) + "\n")
                if not code == constants.NO_COUNTRY_KEY:
                    print("warning country " + code + " not found!")
        print("wrote to", path)


def main():
    data = scrapLeaderboard()
    df = writeLeaderboardToCSV(data)
    count_dict = countCountries(df)
    writeCountryStatsCSV(count_dict)


if __name__ == "__main__":
    main()
