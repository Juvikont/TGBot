from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from repository.config import Base, Session


class Payment(Base):
    __tablename__ = 'payment'
    payment_id = Column(Integer, primary_key=True)
    payment_yandex_id = Column('payment_yandex_id', String)
    payment_status = Column('payment_status', String)
    payment_amount = Column('payment_amount', Numeric)
    payment_currency = Column('payment_currency', String)
    payment_idempotency_key = Column('payment_idempotency_key', String)
    payment_date = Column('payment_date', Date)
    payment_product = Column('payment_product', Integer, ForeignKey('products.id'))
    payment_customer = Column('payment_customer', Integer)
    product = relationship('repository.product_repository.Product')

    # cart_payment = Column('cart_payment', Integer, ForeignKey('shopping_cart.cart_id'))

    def __init__(self, payment_yandex_id, payment_status, payment_amount, payment_currency, payment_idempotency_key,
                 payment_date, payment_product, payment_customer):
        self.payment_yandex_id = payment_yandex_id,
        self.payment_status = payment_status,
        self.payment_amount = payment_amount,
        self.payment_currency = payment_currency,
        self.payment_idempotency_key = payment_idempotency_key,
        self.payment_date = payment_date,
        self.payment_product = payment_product,
        self.payment_customer = payment_customer

    def __repr__(self):
        return "<Payment(payment_id= {},payment_yandex_id='{}', payment_status='{}', payment_amount={}," \
               "payment_currency={}," \
               "payment_idempotency_key={},payment_date={},payment_product = {}, payment_customer = {} >\n" \
            .format(self.payment_id, self.payment_yandex_id, self.payment_status, self.payment_amount,
                    self.payment_currency, self.payment_idempotency_key, self.payment_date, self.payment_product,
                    self.payment_customer)


def get_all_payments():
    s = Session()
    return s.query(Payment).all


def get_payment_status(status):
    s = Session()
    return s.query(Payment).filter(Payment.payment_status == status).first()


def add_payment(payment):
    s = Session()
    s.add(payment)
    s.commit()


def get_payment_by_customer(customer):
    s = Session()
    return s.query(Payment).filter(Payment.payment_customer == customer).all()


def get_payment_by_payment_yandex_id(payment_yandex_id):
    s = Session()
    return s.query(Payment).filter(Payment.payment_yandex_id == payment_yandex_id).first()


def update_payment_status(payment_status, payment_id):
    s = Session()
    statustoupdate = {Payment.payment_status: payment_status}
    paymenttoupdate = s.query(Payment).filter(Payment.payment_yandex_id == payment_id)
    paymenttoupdate.update(statustoupdate)
    s.commit()


def get_payment_by_payment_id(payment_id):
    s = Session()
    return s.query(Payment).filter(Payment.payment_id == payment_id).first()
