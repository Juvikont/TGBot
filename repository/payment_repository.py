from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from repository.config import Base, Session


class Payment(Base):
    __tablename__ = 'payment'
    payment_id = Column(Integer, primary_key=True)
    payment_status = Column('payment_status', Boolean, default=False)
    payment_amount = Column('payment_amount', Numeric)
    payment_check_sum = Column('payment_check_sum', String)
    cart_payment = Column('cart_payment', Integer, ForeignKey('shopping_cart.cart_id', passive_deletes=True))
    products = relationship('repository.shopping_cart_repository.ShoppingCart')

    def __init__(self, payment_status, payment_amount, payment_check_sum, cart_payment):
        self.payment_status = payment_status
        self.payment_amount = payment_amount
        self.payment_check_sum = payment_check_sum
        self.cart_payment = cart_payment

    def __repr__(self):
        return "<Payment(payment_id='{}', payment_status='{}', payment_amount={},payment_check_sum={} >\n" \
            .format(self.payment_id, self.payment_status, self.payment_amount, self.payment_check_sum)


def get_all_payments():
    s = Session()
    return s.query(Payment).all


def get_payment_status(status):
    s = Session()
    return s.query(Payment).filter(Payment.payment_status == status).first()
