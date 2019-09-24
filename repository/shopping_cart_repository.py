from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from repository.config import Base


class ShoppingCart(Base):
    __tablename__ = 'shopping_cart'
    id = Column('cart_id', Integer, primary_key=True)
    cart_item = Column('cart_item', Integer, ForeignKey('products.id'),)
    cart_quantity = Column('cart_quantity', Integer)
    products = relationship('repository.product_repository.Product', back_populates='cart_items')

    def __init__(self, cart_item, cart_quantity):
        self.cart_item = cart_item
        self.cart_quantity = cart_quantity
