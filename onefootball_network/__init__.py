"""onefootball_network module."""
import logging

from rich.logging import RichHandler

from .client import OneFootballNetwork  # isort: skip


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(RichHandler())
