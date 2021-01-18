import constants as Const
import json
import time
import os
import utils
import pandas as pd


def _leaderboard_to_js(input_path, var_name):
    """
	Reads from the scraped .csv and writes it as a json variable declaration in a .js file

	@param input_path: path to the file to read from
	@param var_name: name of the variable in the generated js file
	@return: a string with the file content as a javascript variable declaration
	"""
    df = pd.read_csv(input_path)
    data_dic = {}
    for i, row in df.iterrows():
        data_dic[row["country"]] = row["total"]

    head_str = "var " + var_name + " = "
    last_updated = "var " + var_name + "_timestamp = " + str(time.time()) + ";"
    return head_str + json.dumps(data_dic) + ";\n" + last_updated


def _write_string_to_file(input, file_path):
    """
	Writes input string to file_path

	@param input: input string
	@param file_path: string with full path to the file to write to
	"""
    utils.create_folder_if_needed(os.path.dirname(file_path))
    with open(file_path, "w") as file:
        file.write(input)
        print("wrote to file " + file_path)


def _build_dataset(name):
    source_path = Const.Files.GENERATED + "/" + Const.Files.COUNTRY_STATS_PREFIX + name + ".csv"
    output_path = Const.Files.WEB_FOLDER + "/" + Const.Files.SCRIPTS_FOLDER + "/" + \
                  Const.Files.DATASET_PREFIX + name + ".js "
    var_name = Const.Files.DATASET_PREFIX + name
    js_string = _leaderboard_to_js(source_path, var_name)
    _write_string_to_file(js_string, output_path)


def build():
    _build_dataset(Const.Regions.AMERICAS)
    _build_dataset(Const.Regions.EUROPE)
    _build_dataset(Const.Regions.SE_ASIA)
    _build_dataset(Const.Regions.CHINA)
