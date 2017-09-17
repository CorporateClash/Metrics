import os
import requests
import json
import certifi
import traceback
import cachet
from enums import ComponentStatus

username = os.environ["username"]
password = os.environ["password"]
login_metric_id = os.environ["login_metric_id"]
website_comp_id = os.environ["website_comp_id"]
login_comp_id = os.environ["login_comp_id"]
mongo_comp_id = os.environ["mongo_comp_id"]
mongo_url = os.environ["mongo_url"]
mongo_username = os.environ["mongo_username"]
mongo_password = os.environ["mongo_password"]

Cachet = cachet.cachet()

def handle_login():
    data = {'u': username, 'p': password}
    req = requests.post('https://projectaltis.com/api/login', json=data, verify=certifi.where())
    print("Api returned " + str(req.status_code) + " in seconds: " + str(int(req.elapsed.seconds)))
    # report metric no matter what
    Cachet.report_login_time(req.elapsed.microseconds / 1000, login_metric_id)
    status = ComponentStatus.operational
    # report performance issue
    if req.elapsed.seconds > 3:
        status = ComponentStatus.performanceIssues
    if req.status_code != 200:
        status = ComponentStatus.majorOutage
    try:
        json.loads(req.text)
    except:
        # Major outage if it's not some json
        status = ComponentStatus.majorOutage
    Cachet.report_component(status, login_comp_id)

def handle_website():
    req = requests.get("https://www.projectaltis.com", headers={'User-Agent': 'Mozilla/5.0'})
    print("Website returned " + str(req.status_code) + " in seconds: " + str(int(req.elapsed.seconds)))

    status = ComponentStatus.operational
    if req.elapsed.seconds > 3:
        status = ComponentStatus.performanceIssues
    if req.status_code != 200:
        status = ComponentStatus.majorOutage
    Cachet.report_component(status, website_comp_id)

def handle_mongo():
    req = requests.get(mongo_url, headers={'User-Agent': 'Mozilla/5.0'}, auth=(mongo_username, mongo_password))
    print("Mongo returned " + str(req.status_code) + " in seconds: " + str(int(req.elapsed.seconds)))

    status = ComponentStatus.operational
    if req.elapsed.seconds > 3:
        status = ComponentStatus.performanceIssues
    if req.status_code != 200:
        status = ComponentStatus.majorOutage
    Cachet.report_component(status, mongo_comp_id)


def lambda_handler(event, context):
    try:
        handle_login()
        handle_website()
        handle_mongo()
    except:
        print(traceback.format_exc())