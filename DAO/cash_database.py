import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Column, String, Float, Integer
from sqlalchemy.orm import sessionmaker

metadata = MetaData()
engine = create_engine('sqlite:///app', echo=True)
Base = declarative_base()
db_session = sessionmaker(bind=engine)()


class PaymentModel(Base):
    __tablename__ = 'payment'

    payment_id = Column(String(100), primary_key=True)
    item_sum = Column(Float,nullable=False)
    item_name = Column(String(250), nullable=False)
    order_id = Column(String(250), nullable=False)
    paid_date = Column(String(250), nullable=False)
    created_date = Column(String(250), nullable=False)
    status = Column(String(50), nullable=False)
    session_id = Column(String(100), nullable=False)
    text_status = Column(String(100), nullable=False)


    def dictionarize(self):
        return {

            "payment_id": self.payment_id,
            "item_sum": self.item_sum,
            "item_name": self.item_name,
            "order_id": self.order_id,
            "paid_date": self.paid_date,
            "created_date": self.created_date,
            "status": self.status,
            "session_id": self.session_id,
            "text_status": self.text_status,

        }


class ReceiptModel(Base):
    __tablename__ = 'receipt'

    payment_id = Column(Integer, primary_key=True)
    item_sum = Column(Float,nullable=False)
    item_name = Column(String(250), nullable=False)
    receipt_date = Column(String(250), nullable=False)
    lsc = Column(String(250), nullable=False)

    def dictionarize(self):
        return {

            "payment_id": self.payment_id,
            "item_sum": self.item_sum,
            "item_name": self.item_name,
            "receipt_date": self.receipt_date,
            "lsc": self.lsc,

        }