"""Pydantic models for OneFootball Network API."""
import warnings

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from lxml import html  # noqa: S410, we trust incoming HTML
from pydantic import BaseModel, HttpUrl, validator
from pydantic.fields import Field


class LoginResponse(BaseModel):
    """Login response containing authentication token."""

    access_token: str


class Language(str, Enum):
    """Supported languages for OneFootball Network API."""

    br = "br"
    de = "de"
    en = "en"
    es = "es"
    fr = "fr"
    id = "id"
    it = "it"
    ko = "ko"
    pt = "pt"
    ru = "ru"


class HtmlBody(str):
    """Partial validation for HTML bodies of articles.

    Ref:
        - https://pydantic-docs.helpmanual.io/usage/types/#classes-with-__get_validators__
        - https://static.onefootball.com/onefootball-network/technical-documentation/html-guidelines
    """

    @classmethod
    def __get_validators__(cls):
        """Yield sequence of validators for pydantic.

        One or more validators may be yielded which will be called in the
        order to validate the input, each validator will receive as an input
        the value returned from the previous validator.

        Yields:
            sequence of field validations.
        """
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")
        tree = html.fromstring(v)

        unsupported_types = [
            c
            for c in tree.getchildren()
            if c.tag
            not in (
                "p",
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
                "hr",
                "a",
                "li",
                "ol",
                "ul",
                "img",
                "blockquote",
                "iframe",
            )
        ]
        for child in unsupported_types:
            warnings.warn(
                f"The following non-supported HTML elements will be ignored: <{child.tag}>", Warning
            )

        return cls(v)


class PostUpdate(BaseModel):
    """Article attributes that can be updated."""

    source_url: HttpUrl = Field(
        ...,
        description="""The link to the article as published on your website.
    Place your homepage url if the article is not published anywhere else.""",
    )
    language: Language = Field(..., description="The language of the article.")
    published: datetime = Field(
        ...,
        description="The time that the article was published. If in doubt, use the current time.",
    )
    modified: Optional[datetime] = Field(
        None,
        description="The time that the article was last updated. If in doubt, use the current time.",
    )
    title: str = Field(..., min_length=1, description="The title of the article.")
    content: HtmlBody = Field(
        ...,
        description="""The content of the article, which must be in correctly-formatted HTML.
        Please see [this link](https://static.onefootball.com/onefootball-network/technical-documentation/html-guidelines)
        for important details on acceptable HTML content.""",
    )
    image_url: Optional[HttpUrl] = Field(
        None, description="An optional field for the URL of the article’s featured image."
    )
    image_width: Optional[int] = Field(None, description="The image’s width in pixels.")
    image_height: Optional[int] = Field(None, description="The image’s height in pixels.")
    breaking_news: Optional[bool]

    @validator("image_url", "image_width", "image_height", pre=True)
    def override_default(cls, v) -> Optional[Union[str, int]]:
        """Handle misleading defaults sent by backend.

        Defaults: 'image_url': '', 'image_width': 0, 'image_height': 0
        """
        if not v:
            return None
        return v

    @validator("image_width", "image_height")
    def is_provided_with_image_url(cls, v, values) -> int:
        """If image_url is provided, image_width and image_height should be provided as well."""
        img_url = values.get("image_url")
        if img_url and not v:
            raise ValueError(
                "If image_url is provided, image_width and image_height should be provided as well."
            )
        return v

    class Config:
        """Custom model config."""

        use_enum_values = True
        json_encoders = {
            # ISO 8601, %z should work according to https://en.wikipedia.org/wiki/ISO_8601
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }


class NewPost(PostUpdate):
    """A new post payload."""

    external_id: str = Field(
        ...,
        description="""The ID of the article as defined in your system.
        It must be unique (within a given language) within your own system.""",
    )
    draft: Optional[bool] = Field(
        False,
        description="""An optional boolean to be used for testing purposes.
        If set to True, the article will not be made visible to OneFootball users.
        If not povided, the article will by default be made available to OneFootball users.""",
    )


class DetailedPost(NewPost):
    """A single published post."""

    onefootball_id: str = Field(
        ...,
        alias="id",
        description="The ID of the article as defined in the OneFootball Network API system.",
    )
    synced: bool


class PostsResponse(BaseModel):
    """Multiple published posts."""

    posts: List[DetailedPost]
