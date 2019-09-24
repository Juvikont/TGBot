from repository.config import engine,Base
from sqlalchemy.orm import sessionmaker
from repository.product_repository import Product
from repository.shopping_cart_repository import ShoppingCart
from repository.product_photos_repository import ProductPhoto


Session = sessionmaker(bind=engine)


def remade_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


tshirt = Product(
    product_name='Calvin Kleine',
    product_description='Geniune silk',
    product_price=65,
    product_quantity=1,
    product_type='Thirt',
    product_sex='Male')

Base.metadata.create_all(engine)
s = Session()
s.add(tshirt)
s.commit()
