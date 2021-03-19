FROM debian:10-slim

# All the apt
RUN apt update && apt install -y --no-install-recommends \
	python3 \
	python3-pip \
	firefox-esr

# Python packages
COPY requirements.txt service_config/
RUN pip3 install -r service_config/requirements.txt

# Copy project
COPY . /app
WORKDIR /app

# Webdriver needed for selenium
RUN mv geckodriver /usr/local/bin/
RUN chmod 555 /usr/local/bin/geckodriver

# REMOVE LATER google app credentials
# COPY service-account.json /service_config/
# ENV GOOGLE_APPLICATION_CREDENTIALS=/service_config/service-account.json
WORKDIR service/

CMD gunicorn -w 1 -b "0.0.0.0:${PORT:-8080}" --timeout 360 \
 --keep-alive 360 --graceful-timeout 60 "main:create_service()"