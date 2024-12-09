
from config.app_config import settings
import sentry_sdk

def init_sentry():
    if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
        sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)