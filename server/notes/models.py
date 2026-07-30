from typing import List, Optional

from pydantic import Field
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

from helpers import CustomBaseModel, is_valid_filename, strip_whitespace
from global_config import Visibility


class NoteBase(CustomBaseModel):
    title: str


class NoteCreate(CustomBaseModel):
    title: Annotated[
        str,
        AfterValidator(strip_whitespace),
        AfterValidator(is_valid_filename),
    ]
    content: Optional[str] = Field(None)
    visibility: Optional[Visibility] = Field(Visibility.PRIVATE)


class Note(CustomBaseModel):
    title: str
    content: Optional[str] = Field(None)
    last_modified: float
    visibility: Visibility = Visibility.PRIVATE


class NoteUpdate(CustomBaseModel):
    new_title: Annotated[
        Optional[str],
        AfterValidator(strip_whitespace),
        AfterValidator(is_valid_filename),
    ] = Field(None)
    new_content: Optional[str] = Field(None)
    visibility: Optional[Visibility] = Field(None)


class SearchResult(CustomBaseModel):
    title: str
    last_modified: float
    score: Optional[float] = Field(None)
    title_highlights: Optional[str] = Field(None)
    content_highlights: Optional[str] = Field(None)
    tag_matches: Optional[List[str]] = Field(None)
    visibility: Visibility = Visibility.PRIVATE
