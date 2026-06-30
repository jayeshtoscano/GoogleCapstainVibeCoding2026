"""
------------------------------------------------------------
Logger Utility (Gatekeeper AI Platform)
------------------------------------------------------------

Purpose:
- Centralized logging for all agents
- Structured logs for observability systems
- MCP + multi-agent trace support
------------------------------------------------------------
"""

import logging
import json
import sys
from datetime import datetime


##########################################################
# JSON Formatter
##########################################################

class JsonFormatter(logging.Formatter):

    def format(self, record):

        log_record = {

            "timestamp": datetime.utcnow().isoformat(),

            "level": record.levelname,

            "module": record.name,

            "message": record.getMessage()

        }

        return json.dumps(log_record)


##########################################################
# Logger Factory
##########################################################

def get_logger(name: str = "gatekeeper"):

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if not logger.handlers:

        handler = logging.StreamHandler(sys.stdout)

        handler.setFormatter(JsonFormatter())

        logger.addHandler(handler)

    return logger


##########################################################
# Global Logger
##########################################################

logger = get_logger()
