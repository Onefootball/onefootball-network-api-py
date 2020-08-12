"""onefootball_network module."""
# isort: skip-file
import logging

from rich.logging import RichHandler


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(RichHandler())

from onefootball_network.client import OneFootballNetwork
from onefootball_network.models import DetailedPost, NewPost, PostsResponse, PostUpdate
