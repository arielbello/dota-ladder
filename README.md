Dota Ladder Statistics
======================

A project to create a simple website displaying updated statistics from [Dota 2 leaderboards].
Here's a [running example].

[Dota 2 leaderboards]: http://www.dota2.com/leaderboards
[running example]: https://arielbello.github.io/dota-ladder/

How it works
----------------------
This is currently a container solution designed to work on Google Cloud Platform. 
(Don't worry, free tier services are enough to run it).

For the example, in the link above, I built a Docker image and used it on Cloud Run.
When the image first runs, it creates the website structure on a Cloud Storage Bucket.
Then I set up a scheduler to run its updating service. Finally, I made all the website
files available publicly.

Specifically for the Github page, there's a different structure. You may use the
files in the *Storage Bucket* directly, or set up another method to access and display them as I did.

Configuration
----------------------
This code requires some configuration to work.

### Locally

1. Install the required python packages `pip install -r requirements.txt`
1. Set up your selenium environment. This code uses *Firefox* and *gecko*. Refer to [selenium docs] on how to. 
   If you're using *Chrome*, you must make a few code changes
1. In the *service* folder you will find *country_iso_scraper.py* and *leaderboard_scraper.py*. The first scrapes
Wikipedia for country codes and respective names, the second scrapes the actual leaderboards.
1. *service/webpage_builder.py* uses the .csv files created by the scripts above to generate .js datasets
1. Running the scripts in aforementioned order should be enough to create all the files required to properly 
display the website
   
   
### Using Google Cloud:

1. Create a Storage Bucket for this project
1. Build the Docker image and upload it to GCP
1. Create a Cloud Run service and select this image. Set an environment variable `STORAGE_BUCKET = <your-bucket-name>`
1. Set up a Scheduler to perform a GET request on the service endpoint */run-service*
1. Serve the webpage files that are now available in the bucket you created.


License
---------------------
This project is available under the [MIT license](https://opensource.org/licenses/MIT).

[selenium docs]: https://www.selenium.dev/documentation/en/getting_started_with_webdriver/browsers/