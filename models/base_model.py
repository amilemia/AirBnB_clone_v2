#!/usr/bin/python3
"""This module defines the BaseModel class"""

from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
Base = declarative_base()


class BaseModel:
    """Defines all common attributes/methods for other classes"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance"""
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        for key, value in kwargs.items():
            if key != "__class__":
                setattr(self, key, value)

    def __str__(self):
        """Return a string representation of the BaseModel instance"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__
        )

    def save(self):
        """Update updated_at attribute with datetime, save to storage"""
        self.updated_at = datetime.utcnow()
        from models import storage
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return a dictionary representation of the BaseModel instance"""
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        obj_dict.pop('_sa_instance_state', None)  # Remove SQLAlchemy state
        return obj_dict

    def delete(self):
        """Delete the current instance from storage"""
        from models import storage
        storage.delete(self)
