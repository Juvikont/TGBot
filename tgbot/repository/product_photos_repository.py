from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Binary
from tgbot.repository.connect_db import Base


class ProductPhoto(Base):
    __tablename__ = 'product_photos'
    photo_id = Column(Integer, primary_key=True)
    photo_name = Column('product_name', String)
    photo_ext = Column('photo_ext', String(4))
    photo_content = Column('photo_content', Binary)
    is_main = Column('is_true', Boolean,default=False)
    product_id = Column('product_id', ForeignKey('products.id'))

    def __int__(self, photo_name,photo_ext,photo_content,product_id):
        self.photo_name = photo_name
        self.photo_ext = photo_ext
        self.photo_content = photo_content
        self.product_id = product_id
