
from sqlalchemy import Column, DateTime, func, Integer

from app.setup.db import db

class Base(db.Model): #type: ignore
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())