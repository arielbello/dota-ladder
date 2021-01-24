import constants as Const
import os
from google.cloud import storage


def _upload_file(file_path, content_type, cache_timeout=3600, bucket_name=None, file_name=None):
    """
	Uploads a file to a google cloud storage bucket.
	Requires prior google credentials setup (automatically done in a gcloud VM)
	"""

    if not bucket_name:
        assert Const.Urls.STORAGE_BUCKET != None, "STORAGE_BUCKET env not set!"
        bucket_name = Const.Urls.STORAGE_BUCKET

    try:
        file_name = file_name if file_name else os.path.basename(file_path)
        # Any of these api calls can raise an error
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        blob = storage.Blob(file_name, bucket)
        blob.cache_control = f"max-age={cache_timeout}"
        with open(file_path, "rb") as file:
            blob.upload_from_file(file, content_type=content_type)

        print(f"successfully uploaded {file_path} as {file_name} to {bucket_name}")
    except Exception as e:
        print(e)


def _upload_dataset_from_region(region):
    content_type = "application/javascript"
    file_name = Const.Files.DATASET_PREFIX + region + ".js"
    src_path = Const.Files.WEB_FOLDER + "/" + Const.Files.SCRIPTS_FOLDER + "/" + file_name
    dst_path = Const.Files.SCRIPTS_FOLDER + "/" + file_name
    _upload_file(src_path, content_type, cache_timeout=60, file_name=dst_path)


def update_datasets():
    _upload_dataset_from_region(Const.Regions.AMERICAS)
    _upload_dataset_from_region(Const.Regions.EUROPE)
    _upload_dataset_from_region(Const.Regions.SE_ASIA)
    _upload_dataset_from_region(Const.Regions.CHINA)


def startup_upload():
    # scripts/script.js
    src_file = Const.Files.WEB_FOLDER + "/" + Const.Files.SCRIPTS_FOLDER + "/" + Const.Files.SCRIPT_JS
    dst_file = Const.Files.SCRIPTS_FOLDER + "/" + Const.Files.SCRIPT_JS
    content_type = "application/javascript"
    _upload_file(src_file, content_type, file_name=dst_file)
    # index.html
    source_path = Const.Files.WEB_FOLDER + "/" + Const.Files.INDEX_HTML
    content_type = "text/html"
    _upload_file(source_path, content_type, file_name=Const.Files.INDEX_HTML)
    # stylesheet
    source_path = Const.Files.WEB_FOLDER + "/" + Const.Files.STYLE_SHEET
    content_type = "text/css"
    _upload_file(source_path, content_type, file_name=Const.Files.STYLE_SHEET)
