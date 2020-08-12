"""Pydantic models tests."""
import json

import pytest

from pydantic import ValidationError

from onefootball_network.models import NewPost


def test_empty_titles_raise_error():
    """It refuses empty titles."""
    with open("data/clermont_foot_articles.json", "r") as fh:
        articles_raw = json.load(fh)
    articles_raw[0]["title"] = ""

    with pytest.raises(ValidationError) as e:
        _ = NewPost(**articles_raw[0])

    assert "at least 1 characters" in str(e.value)


def test_url_without_hight_raise_error():
    """It refuses image URL without image dimensions."""
    with open("data/clermont_foot_articles.json", "r") as fh:
        articles_raw = json.load(fh)
    articles_raw[1]["image_height"] = None

    with pytest.raises(ValidationError) as e:
        _ = NewPost(**articles_raw[1])

    assert (
        "If image_url is provided, image_width and image_height should be provided as well."
        in str(e.value)
    )


def test_invalid_html_warns():
    """It warns about ignored HTML tags."""
    with open("data/clermont_foot_articles.json", "r") as fh:
        articles_raw = json.load(fh)
    articles_raw[0]["content"] += " <table>With some data</table>"

    with pytest.warns(Warning) as record:
        _ = NewPost(**articles_raw[0])

    assert len(record) == 1
    assert (
        record[0].message.args[0]
        == "The following non-supported HTML elements will be ignored: <table>"
    )
