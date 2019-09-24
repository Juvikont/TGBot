from tgbot.repository.connect_db import Base, Session, engine
from tgbot.repository.product_photos_repository import ProductPhoto
from tgbot.repository.payment_repository import Payment
from tgbot.repository.product_repository import Product
from tgbot.repository.shopping_cart_repository import ShoppingCart

Base.metadata.create_all(engine)
session = Session()

