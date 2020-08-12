"""Pydantic models for OneFootball Network API."""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, HttpUrl


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


class NewPost(BaseModel):
    """A new post payload."""

    external_id: str
    source_url: HttpUrl
    language: Language
    published: datetime
    modified: Optional[datetime]
    title: str
    content: str
    image_url: Optional[HttpUrl]
    image_width: Optional[int]
    image_height: Optional[int]
    breaking_news: Optional[bool]
    draft: Optional[bool] = False

    class Config:
        """Custom model config."""

        use_enum_values = True
        json_encoders = {
            # ISO 8601, %z should work according to https://en.wikipedia.org/wiki/ISO_8601
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }


class DetailedPost(NewPost):
    """This is not a complete post response specification."""

    id: int
    synced: bool


class PostsResponse(BaseModel):
    """Multiple published posts."""

    posts: List[DetailedPost]
