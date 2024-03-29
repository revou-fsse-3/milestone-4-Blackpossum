from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import relationship,mapped_column
from models.base import Base
from models.Account import Accounts

# password encryption
from flask_login import UserMixin
import bcrypt

class Users(Base,UserMixin):
    __tablename__ = 'Users'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(255), unique=True, nullable=False)
    email = mapped_column(String(255), unique=True, nullable=False)
    password_hash = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Define relationships
    accounts = relationship('Accounts', back_populates='user')

    def set_password(self, plaintext_password):
        self.password_hash = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # Store the hash as a string

    def check_password(self,password):
        # check password from bcrypt package
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))


    def __repr__(self):
        return f"<Users(id={self.id}, username={self.username}, email={self.email}, created_at={self.created_at}, updated_at={self.updated_at})>"
