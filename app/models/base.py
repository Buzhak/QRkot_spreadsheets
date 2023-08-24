from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.orm import validates

from app.models.error_hendlers import int_not_zero_or_less


class BaseModel:
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None)

    @validates(full_amount)
    def validate_full_amount(self, key, value):
        return int_not_zero_or_less(key, value)
