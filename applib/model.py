

import records
from contextlib import contextmanager
from sqlalchemy import (create_engine, Integer, String,
                        Text, DateTime, BigInteger, Date, DECIMAL,
                        Column, ForeignKey, or_, Sequence, func,
                        PrimaryKeyConstraint,
                        ForeignKeyConstraint, Index
                        )

import sqlalchemy.dialects.postgresql as ptype
 

from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from applib.lib import helper as h 

from flask_login import UserMixin

import os


from datetime import datetime

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

con_str = h.set_db_uri()
Engine = create_engine(con_str, echo=True, pool_size=100)
Base = declarative_base()


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

@contextmanager
def db_session():
    db = records.Database(con_str, echo=True)
    conn = db.get_connection()
    tx = conn.transaction()

    try:    
        yield conn
        tx.commit()
    
    except Exception as e:
        tx.rollback()
        raise e 
        # log the error here 
    
    finally:
        conn.close()

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

@contextmanager  
def sql_cursor():

    Cursor = sessionmaker(Engine)
    session = Cursor()

    try:         
        yield session
        session.commit()
    except Exception as e:  
        session.rollback()
        raise e 

        # if in dev environment raise error else log to file or smtp.
        
        # if os.getenv("env", None) == 'dev':
        #     raise e

        # lg = logs.get_logger('db_error', is_debug=True)
        # lg.exception(g.domain)
        
    finally:
        session.close()

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

class Users(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(BigInteger, Sequence('users_id_seq'), primary_key=True)    
    username = Column(String(150), nullable=True)
    password = Column(String(150), nullable=True)     


class Invoice(Base):

    __tablename__ = "invoice"

    id = Column(BigInteger, Sequence('invoice_inv_id_seq'), primary_key=True)    
    disc_type = Column(String(10))    
    disc_value = Column(String(10)) 
    disc_desc = Column(Text)  
    purchase_no = Column(Integer)  
    invoice_no = Column(String(30))   
    date_value = Column(DateTime())  
    invoice_due = Column(DateTime())
    client_type = Column(Integer, nullable=False)
    currency  = Column(Integer, nullable=False) 
    client_id =  Column(BigInteger, ForeignKey('client.id'), nullable=False)
    payment = relationship('Payment', backref='client', lazy=True)
    item = relationship('Items', backref='invoice', lazy=True)
    is_dummy = Column(Integer)

    recurrent_bill_id = Column(BigInteger, ForeignKey('recurrent_bill.id'), nullable=True)

    view_count: Mapped[int]
    last_view: Mapped[datetime]
    


class Items(Base):

    __tablename__ = "item"

    id = Column(BigInteger, Sequence('item_id_seq'), primary_key=True) 
    item_desc = Column(String(150), nullable=False)
    qty = Column(Integer, nullable=False)
    rate = Column(Integer, nullable=False)
    amount = Column(DECIMAL(15,2))
    invoice_id = Column(BigInteger, ForeignKey('invoice.id'),
        nullable=False)


class EmailQueue(Base):

    __tablename__ = "email_queue"

    id = Column(BigInteger, Sequence('email_queue_id_seq'), primary_key=True)
    field= Column(String(150))
    reference= Column(String(150))
    date_created= Column(DateTime())
    status= Column(Integer)


class Client(Base):
    
    __tablename__ = "client"

    id = Column(BigInteger, Sequence('client_invoice_id_seq'), primary_key=True)
    name = Column(String(150), nullable=False)
    address = Column(Text, nullable=False)    
    email = Column(String(150), nullable=False) 
    phone = Column(String(25), nullable=False)        
    post_addr = Column(String(20), nullable=False) 
    date_created = Column(DateTime(), nullable=False)
    invoice = relationship('Invoice', backref='client', lazy=True)
 


class Expense(Base):

    __tablename__ = "expense"

    id = Column(BigInteger, Sequence('expense_id_seq'), primary_key=True)
    title = Column(String(100))
    desc = Column(Text)
    date_created = Column(DateTime, nullable=False, 
                          default=datetime.now())
    
    requested_by = Column(String(100), nullable=False)

    # status =1 for pending, 2 for approved and 3 for declined 
    status = Column(Integer, nullable=False, default=0)
    aproved_by = Column(String(100), nullable=False)
    amount = Column(DECIMAL(15, 2), nullable=False)
    
    # 2, salary payment, 3 bonus payment
    # 4 miscellinous payments  and 5 vat remittance payments 
    
    payment_type =Column(Integer)  # 1 for Office expenses 


class Payment(Base):

    __tablename__ = 'payment'

    id = Column(BigInteger, Sequence('payment_id_seq'), primary_key=True)
    client_name = Column(String(150), nullable=False)
    payment_desc = Column(Text)
    date_created = Column(DateTime, nullable=False, default=datetime.now())
    payment_mode = Column(Integer, nullable=False)
    amount_paid: Mapped[float] = Column(DECIMAL(15, 2))
    balance = Column(DECIMAL(15,2))
    invoice_id = Column(BigInteger,ForeignKey('invoice.id'), nullable=False)
    status = Column(Integer, nullable=False, default=0)
    view_count: Mapped[int]
    last_view: Mapped[datetime]


class EmailReceipt(Base):

    __tablename__ = 'email_receipt_count'

    id = Column(BigInteger, Sequence('email_receipt_id_seq'), primary_key=True)
    ref = Column(String(240), nullable=False)
    counter = Column(BigInteger, nullable=False)
    last_received = Column(DateTime, nullable=False)
    body = Column(String(240))



class RecurrentBill(Base):

    class STATUSTYPE():
        pending = 0
        cancelled = -1 
        processed = 1
        in_progress = 2


    __tablename__ = 'recurrent_bill'
    __table_args__ = (
        Index('recurrent_bill_args_req', 'id', 'client_id'),
        Index('recurrent_bill_invoice_req', 'id', 'invoice_id'),          
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(["client_id"], ["client.id"]),        
    )

    id: Mapped[int]
    client_id: Mapped[int] 
    invoice_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('invoice.id'), nullable=True)
    product_name: Mapped[str]
    amount_expected: Mapped[float]
    date_created: Mapped[datetime]
    date_due: Mapped[datetime]
    date_updated: Mapped[datetime]
    payment_status: Mapped[int]



def form2model(formobj, model_ins):
    counter = 0            
    for key, obj in formobj._fields.items():
        if hasattr(model_ins, key):
            setattr(model_ins, key, obj.data)
            counter += 1 

    assert counter > 0 , "No model instance fields not found."
     
def model2form(model_ins, form_ins):

    counter = 0
    for key, obj in form_ins._fields.items():
        if hasattr(model_ins, key):
            obj.data = getattr(model_ins, key)
            counter += 1

    assert counter > 0 , "No model instance fields not found."


def create_tables():
    Base.metadata.create_all(Engine)

def drop_tables():
    Base.metadata.drop_all(Engine)
