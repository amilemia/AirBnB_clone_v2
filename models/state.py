#!/usr/bin/python3
"""This module defines the State class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """State class that inherits from BaseModel"""

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    # For DBStorage
    cities = relationship("City", backref="state",
                          cascade="all, delete-orphan")
