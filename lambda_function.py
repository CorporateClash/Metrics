import os
import requests
import json
import certifi
import traceback
import cachet
import sentry
from enums import ComponentStatus, user_agent

login_username = os.environ.get("login_username", '')
login_password = os.environ.get("login_password", '')
login_endpoint = os.environ.get("login_endpoint", '')
login_metric_id = os.environ.get("login_metric_id", '')
login_comp_id = os.environ.get("login_comp_id", '')

website_comp_id = os.environ.get("website_comp_id", '')
website_endpoint = os.environ.get("website_endpoint", '')

mongo_comp_id = os.environ.get("mongo_comp_id", '')
mongo_url = os.environ.get("mongo_url", '')
mongo_username = os.environ.get("mongo_username", '')
mongo_password = os.environ.get("mongo_password", '')

Cachet = cachet.cachetHandler()

def handle_login():
    if '' in [login_username, login_password, login_metric_id, login_comp_id, login_endpoint]:
        return
    status = ComponentStatus.operational
    try:
        data = {'username': login_username, 'password': login_password}
        req = requests.post(login_endpoint, headers={'User-Agent': user_agent}, json=data, timeout=10)
        print("Api returned " + str(req.status_code) + " in microseconds: " + str(int(req.elapsed.microseconds)))
        # report metric no matter what
        Cachet.report_login_time(int(req.elapsed.microseconds) / 1000, login_metric_id)
        # report performance issue
        if req.elapsed.seconds > 3:
            import cache
            if cache.present('login_slow'):
                status = ComponentStatus.performanceIssues
                cache.delete('login_slow')
            else:
                cache.create('login_slow')
        if req.status_code != 200:
            status = ComponentStatus.majorOutage
        try:
            json.loads(req.text)
        except:
            # Major outage if it's not some json
            status = ComponentStatus.majorOutage
    except:
        print(traceback.format_exc())
        sentry.do()
        status = ComponentStatus.majorOutage
    return Cachet.report_component(status, login_comp_id)

def handle_website():
    if '' in [website_endpoint, website_comp_id]:
        return
    status = ComponentStatus.operational
    try:
        req = requests.get(website_endpoint, headers={'User-Agent': user_agent}, timeout=10)
        print("Website returned " + str(req.status_code) + " in microseconds: " + str(int(req.elapsed.microseconds)))
        if req.elapsed.seconds > 3:
            import cache
            if cache.present('website_slow'):
                status = ComponentStatus.performanceIssues
                cache.delete('website_slow')
            else:
                cache.create('website_slow')
        if req.status_code != 200:
            status = ComponentStatus.majorOutage
    except:
        print(traceback.format_exc())
        sentry.do()
        status = ComponentStatus.majorOutage
    return Cachet.report_component(status, website_comp_id)

def handle_mongo():
    if '' in [mongo_comp_id, mongo_url, mongo_username, mongo_password]:
        return
    status = ComponentStatus.operational
    try:
        req = requests.get(mongo_url, headers={'User-Agent': 'Mozilla/5.0'}, auth=(mongo_username, mongo_password), timeout=5)
        print("Mongo returned " + str(req.status_code) + " in seconds: " + str(int(req.elapsed.seconds)))
        if req.elapsed.seconds > 3:
            import cache
            if cache.present('mongo_slow'):
                status = ComponentStatus.performanceIssues
                cache.delete('mongo_slow')
            else:
                cache.create('mongo_slow')
        if req.status_code != 200:
            status = ComponentStatus.majorOutage
    except:
        print(traceback.format_exc())
        sentry.do()
        status = ComponentStatus.majorOutage
    Cachet.report_component(status, mongo_comp_id)


def lambda_handler(event, context):
    try:
        handle_login()
        handle_website()
        handle_mongo()
    except:
        print(traceback.format_exc())
        sentry.do()
