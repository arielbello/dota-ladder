import constants
import json
import time
import pandas as pd

def leaderboardToJS(input_path, var_name):
	'''
	Reads from the scraped .csv and writes a json variable to a .js file

	@param input_path: path to the file to read from
	@param var_name: name of the variable in the generated js file
	@return: a string with the file content as a javascript variable declaration
	'''
	df = pd.read_csv(input_path)
	data_dic = {}
	for i, row in df.iterrows():
		data_dic[row["country"]] = row["total"]

	head_str = "var " + var_name + " = "
	last_updated = "var " + var_name + "_timestamp = " + str(time.time()) + ";"
	return head_str + json.dumps(data_dic) + ";\n" + last_updated

def writeStringToFile(input, file_path):
	'''
	Writes input string to file_path

	@param input: input string
	@param file_path: string with full path to the file to write to
	'''
	with open(file_path, "w") as file:
		file.write(input)
		print("wrote to file " + file_path)

def main():
	#TODO write all different regions
	folder_path = constants.GENERATED_FOLDER + "/"
	source_path = folder_path + constants.COUNTRY_STATS_CSV
	output_path = folder_path + constants.DATASET_AMERICAS + ".js"
	var_name = constants.DATASET_AMERICAS
	js_string = leaderboardToJS(source_path, var_name)
	writeStringToFile(js_string, output_path)

if __name__ == "__main__":
	#execute only if run as script
	main()