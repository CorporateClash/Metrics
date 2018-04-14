import os
from enum import IntEnum

class ComponentStatus(IntEnum):
    "STATUS"
    operational = 1
    performanceIssues = 2
    partialOutage = 3
    majorOutage = 4


user_agent = 'Mozilla/5.0 ClashMetrics/' + os.environ.get('AWS_LAMBDA_FUNCTION_VERSION', '1.0') + ' (' + os.environ.get('AWS_ACCESS_KEY_ID', '') + '; ' + os.environ.get('AWS_REGION', '') + ')'
