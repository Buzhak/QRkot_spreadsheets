from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example='Назввание проекта')
    description: str = Field(..., min_length=1, example='Описание проекта')
    full_amount: PositiveInt = Field(..., example=1)

    @validator('name', 'description')
    def check_str(cls, value):
        if len(''.join(value.split())) == 0:
            raise ValueError(
                'Поле не может стостоять из пробелов'
            )
        return value


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100, example='Новое назввание проекта')
    description: Optional[str] = Field(None, min_length=1, example='Новое описание проекта')
    full_amount: Optional[PositiveInt] = Field(None, example=1)

    class Config:
        extra = Extra.forbid


class CharityProjectDB(BaseModel):
    close_date: Optional[datetime]
    create_date: datetime
    description: str
    full_amount: PositiveInt
    fully_invested: bool
    id: int
    invested_amount: int
    name: str

    class Config:
        orm_mode = True
