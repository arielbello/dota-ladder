from flask import Flask
import time
import country_iso_scraper
import leaderboard_scraper
import webpage_builder
import gcloud_storage_uploader

app = Flask(__name__)


@app.route("/")
def index():
    return '<h1>Dota Leaderboard back-end service</h1>'


@app.route("/run-service")
def run_service():
    time_start = time.time()
    # country_iso_scraper.scrape()
    leaderboard_scraper.scrape()
    webpage_builder.build()
    gcloud_storage_uploader.update_datasets()
    task_time = time.time() - time_start

    return "Success! It only took " + "{0:.1f}".format(task_time) + " seconds"


def create_service():
    gcloud_storage_uploader.startup_upload()
    return app


if __name__ == "__main__":
    create_service()