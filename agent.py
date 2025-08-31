from clients.anthropic_client import AnthropicClient
import logging
from pythonjsonlogger.json import JsonFormatter
import sys
from config import Config
from clients.anthropic_models import Message
from typing import List

# Configure JSON logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(JsonFormatter())
handler.setLevel(logging.INFO)

logger.addHandler(handler)


class Agent:
    def __init__(
        self,
        config: Config,
        aclient: AnthropicClient,
        logger: logging.Logger = None
    ) -> None:
        self.aclient = aclient
        self.config = config
        self.messages = List[Message]
        self.logger = logger or logging.getLogger(__name__)
