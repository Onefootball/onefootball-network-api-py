"""OneFootball Network API client."""
import json

from enum import Enum
from typing import Any, Optional

import requests

from pydantic import BaseSettings, HttpUrl

from onefootball_network import LOGGER
from onefootball_network.models import DetailedPost, LoginResponse, NewPost, PostsResponse


class Settings(BaseSettings):
    """Settings for API client, parsed from environment variables."""

    base_url: HttpUrl = "https://network-api.onefootball.com"
    login: str
    password: str

    class Config:
        """Custom config."""

        env_file = ".env"
        env_file_encoding = "utf-8"


class Endpoint(str, Enum):
    """OneFootball Network endpoints."""

    login = "/v1/login"
    posts = "/v1/posts"


class OneFootballNetwork:
    """OneFootball Network API Client."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialise client."""
        #  If you create a model that inherits from BaseSettings, the model initialiser
        # will attempt to determine the values of any fields not passed as keyword arguments
        # by reading from the environment.
        # (Default values will still be used if the matching environment variable is not set.)
        LOGGER.info("Reading settings from keyword args or from the environment.")
        self.settings = Settings(**kwargs)

        self.base_url = self.settings.base_url
        self.session = requests.Session()

        self._authenticate()

    def _authenticate(self) -> LoginResponse:
        LOGGER.info("Retrieving an authentication token.")
        response = self.session.post(
            f"{self.base_url.value}{Endpoint.login.value}",
            json=dict(login=self.settings.login, password=self.settings.password),
        )
        login_resp = LoginResponse(**response.json())
        self.session.headers.update({"Authorization": f"Bearer {login_resp.access_token}"})
        return login_resp

    def get_article(
        self, external_id: Optional[str] = None, feed_item_id: Optional[str] = None
    ) -> PostsResponse:
        """List all posts created by you.

        When specifying external_id filter, this endpoint is expected to return a single entity most of the time.
        Bear in mind that two posts in two different languages can have the same external ID.

        Arguments:
            external_id: The ID of the post as identified in an external system.
            feed_item_id: A comma separated list of the post feed item IDs.

        Returns:
            A list of Post entities.

        Raises:
            ValueError
            ValueError
        """
        if not external_id and not feed_item_id:
            raise ValueError("A query filter must always be provided.")
        if external_id and feed_item_id:
            raise ValueError("Combining query filters is not allowed.")

        response = self.session.get(
            f"{self.base_url.value}{Endpoint.posts.value}",
            params=dict(external_id=external_id, feed_item_id=feed_item_id),
        )
        return PostsResponse(**response.json())

    def publish_article(self, article: NewPost) -> DetailedPost:
        """Create a single Post entity.

        To use this endpoint, creator account must have an integration of type "push" configured.

        Arguments:
            article: a NewPost object with the data of the article to publish

        Returns:
            published post
        """
        response = self.session.post(
            f"{self.base_url.value}{Endpoint.posts.value}", json=json.loads(article.json())
        )
        return DetailedPost(**response.json())
