import logging
import warnings

from .settings import *

warnings.filterwarnings(
    "ignore",
    r"DateTimeField .* received a naive datetime",
    RuntimeWarning, r'django\.db\.models\.fields')


def filterRemovedInDjango19Warning(record):
    return "RemovedInDjango19Warning" not in record.getMessage()


warn_logger = logging.getLogger('py.warnings')
warn_logger.addFilter(filterRemovedInDjango19Warning)
