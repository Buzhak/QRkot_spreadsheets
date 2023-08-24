from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationBase(BaseModel):
    pass


class DonationCreate(DonationBase):
    full_amount: PositiveInt = Field(..., example=1)
    comment: Optional[str] = Field(None, example='Комментарий для пожертвования, по желанию')


class DonationShortDB(DonationBase):
    comment: Optional[str]
    create_date: datetime
    full_amount: PositiveInt
    id: int

    class Config:
        orm_mode = True


class DonationFullDB(DonationBase):
    comment: Optional[str]
    create_date: datetime
    full_amount: PositiveInt
    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool

    class Config:
        orm_mode = True
