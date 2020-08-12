"""onefootball_network module."""
import logging

from rich.logging import RichHandler

from .client import OneFootballNetwork


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(RichHandler())
