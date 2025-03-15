from typing import List

from pydantic import BaseModel


class KeyModel(BaseModel):
    key: str


class ChangeKeyRequest(BaseModel):
    value: str


class ChangeKeyResponse(BaseModel):
    value: str
    ttl: int


class StateItem(BaseModel):
    size: int
    capacity: int
    items: List[str]
