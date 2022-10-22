from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    pass

from logging import LogRecord
from logging.handlers import SysLogHandler
from loguru import logger


def configure_external_log() -> None:
    handler = SysLogHandler(address=('logs6.papertrailapp.com', 11789))
    logger.add(handler)
