from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from models.base import Base
from models.Account import Accounts

class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Define relationships
    accounts = relationship('Accounts', back_populates='user')

    def __repr__(self):
        return f"<Users(id={self.id}, username={self.username}, email={self.email}, created_at={self.created_at}, updated_at={self.updated_at})>"
