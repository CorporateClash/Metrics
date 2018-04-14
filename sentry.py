import os
import raven

def do():
    sentry_dsn = os.environ.get("sentry_dsn", '')

    if '' == sentry_dsn:
        return
    import raven
    raven_reporter = raven.Client(sentry_dsn)
    raven_reporter.captureException()

do()