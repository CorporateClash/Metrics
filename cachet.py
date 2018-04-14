import os
from datetime import datetime
from enums import user_agent
import requests
import json
import certifi
import traceback
import cachetclient.cachet as cachet

class cachetHandler():

    def __init__(self):
        self._ENDPOINT = os.environ["cachet_endpoint"]  # like https://status.corporateclash.net/api/v1
        self._cachet_token = os.environ["cachet_token"]
        self.points = cachet.Points(endpoint=self._ENDPOINT, api_token=self._cachet_token, user_agent=user_agent)
        self.component = cachet.Components(endpoint=self._ENDPOINT, api_token=self._cachet_token, user_agent=user_agent)

    def report_login_time(self, milliseconds, login_metric_id):
        return self.points.post(id=login_metric_id, value=int(milliseconds), timestamp=int(datetime.utcnow().timestamp()))

    def report_component(self, status_value, component_id):
        return self.component.put(id=component_id, component=component_id, status=int(status_value))