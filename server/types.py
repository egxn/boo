from typing import Union
from pydantic import BaseModel


class User(BaseModel):
    authorization_token: str
    user: str


class Prompt(User, BaseModel):
    prompt: str


class SpeechToText(User, BaseModel):
    speech: str


class Text(User, BaseModel):
    text: str


class TextToText(User, BaseModel):
    lang_source: Union[str, None]
    lang_target: Union[str, None]
    text: str
