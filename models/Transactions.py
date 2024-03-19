from sqlalchemy import Integer, DECIMAL, String, DateTime, ForeignKey,func
from sqlalchemy.orm import relationship, mapped_column
from models.base import Base

class Transactions(Base):
    __tablename__ = 'Transactions'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_account_id = mapped_column(Integer, ForeignKey('Accounts.id'))
    to_account_id = mapped_column(Integer, ForeignKey('Accounts.id'))
    amount = mapped_column(DECIMAL(10, 2), nullable=False)
    type = mapped_column(String(255), nullable=False)
    description = mapped_column(String(255))
    created_at = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Define relationships
    from_account = relationship('Accounts', foreign_keys=[from_account_id], back_populates='transactions_from')
    to_account = relationship('Accounts', foreign_keys=[to_account_id], back_populates='transactions_to')

    def __repr__(self):
        return f"<Transactions(id={self.id}, from_account_id={self.from_account_id}, to_account_id={self.to_account_id}, amount={self.amount}, type={self.type}, description={self.description}, created_at={self.created_at})>"
