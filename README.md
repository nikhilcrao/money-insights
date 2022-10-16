# money-insights

Flask app that allows you to track your spending, build budgets and understand your finances.


## Development Guide

This project uses Flask to build the app. It is setup to use GAE to deploy and host the app.

### Deploying code to GAE

gcloud app deploy


### Opening the app

gcloud app browse


### Commit to git

git push -u origin main


### Setup the virtualenv

python3 -m venv env
source env/bin/activate

pip install -r requirements.txt


### Run the application for local development

python main.py






## Resources

*  https://cloud.google.com/appengine/docs/standard/python3/building-app/writing-web-service
*  https://console.cloud.google.com/datastore/entities
