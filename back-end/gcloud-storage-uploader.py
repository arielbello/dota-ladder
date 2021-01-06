import constants
import os
from google.cloud import storage

def uploadFile(file_path, bucket_name, file_name=None):
	'''
	Uploads a file to a google cloud storage bucket.
	Requires prior google credentials setup (automatically done in a gcloud VM)

	@param file_path: path to file to be uploaded
	@param file_name: optional name for the uploaded file
	@param bucket_name: name for the target storage bucket
	'''
	try:
		file_name = file_name if file_name else os.path.basename(file_path)
		#Any of these api calls can raise an error
		client = storage.Client()
		bucket = client.get_bucket(bucket_name)
		blob = storage.Blob(file_name, bucket)
		with open(file_path, "rb") as file:
			blob.upload_from_file(file)

		print(f"successfuly uploaded {file_path} as {file_name} to {bucket_name}")
	except Exception as e:
		print(e)

def main():
	#TODO every dataset
	path = constants.GENERATED_FOLDER + "/" + constants.DATASET_AMERICAS + ".js"
	uploadFile(path, constants.STORAGE_BUCKET)

if __name__ == "__main__":
	main()