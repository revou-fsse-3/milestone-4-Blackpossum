from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from models.Transactions import Transactions

class Accounts(Base):
    __tablename__ = 'Accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    account_type = Column(String(255), nullable=False)
    account_number = Column(String(255), unique=True, nullable=False)
    balance = Column(DECIMAL(10, 2), nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime, nullable=False)

    # Define relationships
    user = relationship('Users', back_populates='accounts')
    transactions_from = relationship('Transactions', foreign_keys='Transactions.from_account_id', back_populates='from_account')
    transactions_to = relationship('Transactions', foreign_keys='Transactions.to_account_id', back_populates='to_account')

    def __repr__(self):
        return f"<Accounts(id={self.id}, user_id={self.user_id}, account_type={self.account_type}, account_number={self.account_number}, balance={self.balance}, created_at={self.created_at}, updated_at={self.updated_at})>"
