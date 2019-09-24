from sqlalchemy import Column, Integer, String, BigInteger,DECIMAL
from sqlalchemy.orm import relationship
from repository.config import Base



class Product(Base):
    __tablename__ = 'products'
    id = Column(BigInteger, primary_key=True)
    product_name = Column('product_name', String(50))
    product_description = Column('product_description', String(100))
    product_price = Column('product_price', DECIMAL(5))
    product_quantity = Column('product_quantity', Integer)
    product_type = Column('product_type', String(10))
    product_sex = Column('product_sex', String(6))
    cart_items = relationship('repository.shopping_cart_repository.ShoppingCart', back_populates='products')
    photos = relationship('repository.product_photos_repository.ProductPhoto')

    def __init__(self, product_name, product_description,
                 product_price, product_quantity, product_type, product_sex):
        self.product_name = product_name
        self.product_description = product_description
        self.product_price = product_price
        self.product_quantity = product_quantity
        self.product_type = product_type
        self.product_sex = product_sex


