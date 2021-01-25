import constants as Const
import json
import time
import os
import utils
import pandas as pd


def _dataset_to_js(dataset, var_name) -> str:
    """
	Reads from the scraped .csv and writes it as a json variable declaration in a .js file

	@return: a string with the file content as a javascript variable declaration
	"""

    head_str = "var " + var_name + " = "
    last_updated = "var " + var_name + "_timestamp = " + str(time.time()) + ";"

    return head_str + json.dumps(dataset) + ";\n" + last_updated


def _leaderboard_to_dic(input_path) -> dict:
    df = pd.read_csv(input_path)
    data_dic = {}
    for i, row in df.iterrows():
        data_dic[row["country"]] = row["total"]

    return _sorted_dict(data_dic)


def _write_string_to_file(input_str, file_path):
    utils.create_folder_if_needed(os.path.dirname(file_path))
    with open(file_path, "w") as file:
        file.write(input_str)
        print("wrote to file " + file_path)


def _get_input_path(region_name: str) -> str:
    return Const.Files.GENERATED + "/" + Const.Files.COUNTRY_STATS_PREFIX + region_name + ".csv"


def _get_output_path(region_name: str) -> str:
    return Const.Files.WEB_FOLDER + "/" + Const.Files.SCRIPTS_FOLDER + "/" + \
           Const.Files.DATASET_PREFIX + region_name + ".js"


def _sorted_dict(unsorted_dict: dict) -> dict:
    return {key: value for key, value in sorted(unsorted_dict.items(), key=lambda item: item[1], reverse=True)}


def _build_dataset(region_name):
    source_path = _get_input_path(region_name)
    output_path = _get_output_path(region_name)
    var_name = Const.Files.DATASET_PREFIX + region_name
    data_dic = _leaderboard_to_dic(source_path)
    js_string = _dataset_to_js(data_dic, var_name)
    _write_string_to_file(js_string, output_path)

    return data_dic


def _build_global_dataset(datasets: list) -> None:
    """
    Creates a single dataset aggregating all regional servers
    """
    data_dic = {}
    for d in datasets:
        for key in d.keys():
            if key in data_dic:
                data_dic[key] += d[key]
            else:
                data_dic[key] = d[key]
    data_dic = _sorted_dict(data_dic)
    output_path = _get_output_path(Const.Regions.GLOBAL)
    var_name = Const.Files.DATASET_PREFIX + Const.Regions.GLOBAL
    js_string = _dataset_to_js(data_dic, var_name)
    _write_string_to_file(js_string, output_path)


def build():
    datasets = [
        _build_dataset(Const.Regions.AMERICAS),
        _build_dataset(Const.Regions.EUROPE),
        _build_dataset(Const.Regions.SE_ASIA),
        _build_dataset(Const.Regions.CHINA)
    ]
    _build_global_dataset(datasets)
