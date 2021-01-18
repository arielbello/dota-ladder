import constants as Const
import utils
import re
import time
import pandas as pd
from bs4 import BeautifulSoup as Soup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def _scrapLeaderboard(url):
    """
    Scrapes a dota 2 leaderboard and creates a dataframe
    
    @param: the url to be scraped (must have the region parameter)  
    @return: a dataframe with the scraped resutls
    """
    # headless usage
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver_options.add_argument("--disable-extensions")
    driver = webdriver.Firefox(options=driver_options)
    # load site
    driver.get(url)
    WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, "leaderboard_body"))
    # unpredictable results with WebDriverWait, so we force wait
    time.sleep(3)
    # load the page to a BeautifulSoup object, because it's easier to use
    soup = Soup(driver.page_source, "lxml")
    # release driver resources
    driver.close()
    # get all table rows
    rows = soup.find(id="leaderboard_body").find_all("tr")
    data = []
    rank = 0
    errors = 0
    # variables to track progress
    perc25 = len(rows) / 4
    prog_dic = dict([(int(perc25 * idx), str((perc25 * idx * 100) // len(rows)) + "%") for idx in range(1, 5)])
    # loop through all table rows
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

    print("scrapping input errors:", errors)

    return data


def _write_leaderboard(data, region_suffix):
    df = pd.DataFrame(data)
    df.columns = ["rank", "name", "clan", "sponsor", "country iso", "flag link"]
    utils.create_folder_if_needed(Const.Files.GENERATED)
    path = Const.Files.GENERATED + "/" + Const.Files.LEADERBOARD_PREFIX + region_suffix + ".csv"
    df.to_csv(path, index=False)
    print("wrote to", path)
    return df


def _count_countries(df_data):
    counter = {}
    for idx, entry in df_data.iterrows():
        key = entry["country iso"]
        if key:
            # good idea forcing it to be lower for further comparisons
            key = key.lower()
        else:
            key = Const.Keys.NO_COUNTRY_KEY

        if key in counter:
            counter[key] += 1
        else:
            counter[key] = 1

    counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    return dict(counter)


def _write_country_stats(count_dict, region):
    iso_dict = {}
    path = Const.Files.GENERATED + "/" + Const.Files.COUNTRY_ISO
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
    utils.create_folder_if_needed(Const.Files.GENERATED)
    path = Const.Files.GENERATED + "/" + Const.Files.COUNTRY_STATS_PREFIX + region + ".csv"
    with open(path, "w", encoding="utf8") as file:
        file.write("country,total\n")
        for code in count_dict:
            if code in iso_dict:
                file.write(iso_dict[code] + "," + str(count_dict[code]) + "\n")
            else:
                file.write(code + "," + str(count_dict[code]) + "\n")
                if not code == Const.Keys.NO_COUNTRY_KEY:
                    print("warning country " + code + " not found!")
        print("wrote to", path)


def _scrape_region(url, region):
    data = _scrapLeaderboard(url)
    df = _write_leaderboard(data, region)
    count_dict = _count_countries(df)
    _write_country_stats(count_dict, region)

def scrape():
    """
    Download all regions leaderboards and creates the resulting data files
    """
    _scrape_region(Const.Urls.AMERICAS_LEADERBOARD, Const.Regions.AMERICAS)
    _scrape_region(Const.Urls.EUROPE_LEADERBOARD, Const.Regions.EUROPE)
    _scrape_region(Const.Urls.SE_ASIA_LEADERBOARD, Const.Regions.SE_ASIA)
    _scrape_region(Const.Urls.CHINA_LEADERBOARD, Const.Regions.CHINA)