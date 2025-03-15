from typing import List, Optional

from pydantic import BaseModel, field_validator


class GetKeyModel(BaseModel):
    value: str


class ChangeKey(GetKeyModel):
    ttl: Optional[int] = None

    @field_validator('ttl')
    def check_ttl(cls, value):
        if value is not None and value <= 0:
            raise ValueError('ttl must be a positive integer or None')
        return value


class StateItem(BaseModel):
    size: int
    capacity: int
    items: List[str]
