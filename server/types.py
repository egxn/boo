from typing import Union
from pydantic import BaseModel

class User(BaseModel):
    authorization_token: str
    user: str

class Prompt(BaseModel, User):
    prompt: str

class SpeechToText(BaseModel, User):
    speech: str

class Text(BaseModel, User):
    text: str

class TextToText(BaseModel, User):
    lang_source: Union[str, None]
    lang_target: Union[str, None]
    text: str