from sqlalchemy import Column, Integer, DECIMAL, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Transactions(Base):
    __tablename__ = 'Transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_account_id = Column(Integer, ForeignKey('Accounts.id'))
    to_account_id = Column(Integer, ForeignKey('Accounts.id'))
    amount = Column(DECIMAL(10, 2), nullable=False)
    type = Column(String(255), nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, nullable=False)

    # Define relationships
    from_account = relationship('Accounts', foreign_keys=[from_account_id], back_populates='transactions_from')
    to_account = relationship('Accounts', foreign_keys=[to_account_id], back_populates='transactions_to')

    def __repr__(self):
        return f"<Transactions(id={self.id}, from_account_id={self.from_account_id}, to_account_id={self.to_account_id}, amount={self.amount}, type={self.type}, description={self.description}, created_at={self.created_at})>"
