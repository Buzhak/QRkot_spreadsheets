from sqlalchemy import Column, String, Text
from sqlalchemy.orm import validates

from app.core.db import Base
from app.models.base import BaseModel
from app.models.error_hendlers import len_not_null


class CharityProject(Base, BaseModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    @validates(name, description)
    def validate_len(self, key, value):
        return len_not_null(key, value)
