from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    username = Column(String, unique=True, index=True)
    display_name = Column(String)
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
