"""OneFootball Network API client."""
import json

from typing import Optional, Union

import requests

from pydantic import BaseSettings, HttpUrl

from onefootball_network import LOGGER
from onefootball_network.models import (
    DetailedPost,
    LoginResponse,
    NewPost,
    PostsResponse,
    PostUpdate,
)


class Settings(BaseSettings):
    """Settings for API client, parsed from environment variables."""

    base_url: HttpUrl = "https://network-api.onefootball.com"  # type: ignore
    login: str
    password: str

    class Config:
        """Custom config."""

        env_file = ".env"
        env_file_encoding = "utf-8"


class OneFootballNetwork:
    """OneFootball Network API Client."""

    def __init__(self, login: Optional[str] = None, password: Optional[str] = None) -> None:
        """Initialise client.

        Arguments:
            login: email address you use to login on the OneFootball Network portal.
                If left empty, it is read from the `LOGIN` environment variable.
            password: password you use to login on the OneFootball Network portal
                If left empty, it is read from the `PASSWORD` environment variable.

        Example:

        ```python
        # parse LOGIN and PASSWORD environment variables
        of = OneFootballNetwork()
        # or pass them directly
        of = OneFootballNetwork(login="editor@football.com", password="mysecret")
        ```
        """
        #  If you create a model that inherits from BaseSettings, the model initialiser
        # will attempt to determine the values of any fields not passed as keyword arguments
        # by reading from the environment.
        # (Default values will still be used if the matching environment variable is not set.)
        LOGGER.info("Reading settings from keyword args or from the environment.")
        kwargs = {}
        if login:
            kwargs.update({"login": login})
        if password:
            kwargs.update({"password": password})
        self.settings = Settings(**kwargs)

        self.base_url = self.settings.base_url
        self.session = requests.Session()

        self._authenticate()

    def _authenticate(self) -> LoginResponse:
        LOGGER.info("Retrieving an authentication token.")
        response = self.session.post(
            f"{self.base_url}/v1/login",
            json=dict(login=self.settings.login, password=self.settings.password),
        )
        response.raise_for_status()
        login_resp = LoginResponse(**response.json())
        self.session.headers.update({"Authorization": f"Bearer {login_resp.access_token}"})
        return login_resp

    def get_articles(
        self, external_id: Optional[str] = None, feed_item_id: Optional[str] = None
    ) -> PostsResponse:
        """List multiple posts created by you.

        When specifying `external_id` filter, this endpoint is expected to return a single entity most of the time.
        Bear in mind that two posts in two different languages can have the same external ID.

        Arguments:
            external_id: The ID of the post as identified in an external system.
            feed_item_id: A comma separated list of the post feed item IDs.
                `feed_item_id` is neither the `external_id` or the `onefootball_id`.

        Returns:
            the list of retrieved article objects.

        Raises:
            ValueError: When the supplied filter combination is incorrect.

        Example:

        ```python
        of = OneFootballNetwork()
        posts = of.get_articles(external_id="3")
        # or
        posts = of.get_articles(feed_item_id="990949,990967,995846")
        ```
        """
        if not external_id and not feed_item_id:
            raise ValueError("A query filter must always be provided.")
        if external_id and feed_item_id:
            raise ValueError("Combining query filters is not allowed.")

        payload = dict(external_id=external_id, feed_item_id=feed_item_id)
        LOGGER.info("Retrieving articles %s", payload)
        response = self.session.get(f"{self.base_url}/v1/posts", params=payload,)
        response.raise_for_status()
        return PostsResponse(**response.json())

    def get_article(self, onefootball_id: Union[int, str]) -> DetailedPost:
        """Return a single article by its OneFootball Network id.

        Arguments:
            onefootball_id: Article id as defined within the OneFootball Network system

        Returns:
            the article object matching the given ID.

        Example:

        ```python
        of = OneFootballNetwork()
        post = of.get_article(onefootball_id="2454354")
        print(post.title)
        ```
        """
        LOGGER.info("Retrieving article %s", onefootball_id)
        response = self.session.get(f"{self.base_url}/v1/posts/{onefootball_id}")
        response.raise_for_status()
        return DetailedPost(**response.json())

    def publish_article(self, article: NewPost) -> DetailedPost:
        """Publish an article to OneFootball.

        To use this endpoint, the creator account must have an integration of type "push" configured.

        !!! note
            You can use autocompletion on the `NewPost` object to see
            available attributes.
            The data model will take care of all data validation for you,
            so that you can focus on passing your content only.

        Arguments:
            article: a `NewPost` object with the data of the article to publish

        Returns:
            the published post

        Example:

        ```python
        from onefootball_network import OneFootballNetwork, NewPost

        of = OneFootballNetwork()
        article = NewPost(
            external_id="28961",
            source_url="https://www.clermontfoot.com/amical-orleans-clermont-annule/",
            language="fr",
            published="2020-08-10T08:28:58Z",
            title="Amical : Orl\u00e9ans &#8211; Clermont annul\u00e9",
            # fmt: off
            content='''<p>A la demande de l&rsquo;US Orl\u00e9ans, le match amical du mercredi
                12 ao\u00fbt opposant l&rsquo;US Orl\u00e9ans et le Clermont Foot 63 \u00e0 Moulins,
                est annul\u00e9.</p> <p>Le prochain match amical du CF63 est pr\u00e9vu le
                samedi 15 ao\u00fbt contre Grenoble et sera retransmis sur le site de
                La Montagne dans le cadre de notre partenariat.</p>'''
            # fmt: on
        )
        post = of.publish_article(article)
        print(post.onefootball_id)
        ```
        """
        payload = json.loads(article.json())
        LOGGER.info("Publishing article %s", payload)
        response = self.session.post(f"{self.base_url}/v1/posts", json=payload)
        response.raise_for_status()
        LOGGER.info(
            "Article published. Get it by calling %s\n or %s",
            f"GET {self.base_url}/v1/posts?external_id={article.external_id}",
            f"OneFootballNetwork.get_articles(external_id={article.external_id})",
        )
        return DetailedPost(**response.json())

    def update_article(self, onefootball_id: str, article: PostUpdate) -> DetailedPost:
        """Update a single article.

        !!! note
            You can use autocompletion on the `PostUpdate` object to see
            available attributes.
            The data model will take care of all data validation for you,
            so that you can focus on passing your content only.

        Arguments:
            onefootball_id: Article id as defined within the OneFootball Network system
            article: a `PostUpdate` object with the article data

        Returns:
            the published post

        """
        payload = json.loads(article.json())
        LOGGER.info("Updating article %s", payload)
        response = self.session.put(f"{self.base_url}/v1/posts/{onefootball_id}", json=payload)
        response.raise_for_status()
        return DetailedPost(**response.json())

    def delete_article(self, onefootball_id: Union[int, str]) -> bool:
        """Delete one article.

        Arguments:
            onefootball_id: Article id as defined within the OneFootball Network system

        Returns:
            If `True`, the article was deleted successfully

        Example:

        ```python
        of = OneFootballNetwork()
        of.delete_article(onefootball_id="24546")
        ```
        """
        LOGGER.info("Deleting article %s", onefootball_id)
        response = self.session.delete(f"{self.base_url}/v1/posts/{onefootball_id}")
        response.raise_for_status()
        is_deleted = response.status_code == 204
        return is_deleted
