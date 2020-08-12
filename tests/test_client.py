"""API client tests."""
import json

from typing import List

import pytest

from pydantic import parse_obj_as

from onefootball_network.client import OneFootballNetwork
from onefootball_network.models import DetailedPost, NewPost


@pytest.fixture(scope="module")
def of_client() -> OneFootballNetwork:
    """OneFootball Network API client."""  # noqa
    of = OneFootballNetwork()
    return of


@pytest.fixture(scope="module")
def articles() -> List[NewPost]:
    """2 yet-to-be-published articles from www.clermontfoot.com."""
    with open("data/clermont_foot_articles.json", "r") as fh:
        articles_raw = json.load(fh)
    articles = parse_obj_as(List[NewPost], articles_raw)
    return articles


@pytest.fixture(scope="module")  # type: ignore
def article(of_client: OneFootballNetwork, articles: List[NewPost]) -> DetailedPost:
    """One published article."""
    post = of_client.publish_article(articles[0])
    yield post
    of_client.delete_article(post.onefootball_id)


def test_authentication(of_client: OneFootballNetwork) -> None:
    """It retrieves an authentication token."""
    assert "Authorization" in of_client.session.headers.keys()

    token = of_client.session.headers["Authorization"].split("Bearer ")[1]
    assert len(token) > 0


def test_get_articles_cannot_combine_filters(of_client: OneFootballNetwork):
    """It can't get articles with more than one filter type specified."""
    with pytest.raises(ValueError) as e:
        of_client.get_articles(external_id="256", feed_item_id="1,52")

    assert str(e.value) == "Combining query filters is not allowed."


def test_get_articles_has_filters(of_client: OneFootballNetwork):
    """It can't get articles without a fiter."""
    with pytest.raises(ValueError) as e:
        of_client.get_articles()

    assert str(e.value) == "A query filter must always be provided."


def test_get_articles(of_client: OneFootballNetwork, article: DetailedPost):
    """It gets multiple articles."""
    external_id = article.external_id
    post_response = of_client.get_articles(external_id=external_id)
    assert len(post_response.posts) == 1
    assert post_response.posts[0].external_id == external_id


def test_get_article(of_client: OneFootballNetwork, article: DetailedPost):
    """It gets one article."""
    detailed_post = of_client.get_article(onefootball_id=article.onefootball_id)
    assert detailed_post.onefootball_id == article.onefootball_id

    detailed_post = of_client.get_article(onefootball_id=int(article.onefootball_id))
    assert detailed_post.onefootball_id == article.onefootball_id


def test_delete_article(of_client: OneFootballNetwork, articles: List[NewPost]):
    """It deletes one article."""
    post = of_client.publish_article(articles[1])
    assert of_client.delete_article(post.onefootball_id)
