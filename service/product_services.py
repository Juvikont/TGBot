from repository.payment_repository import get_all_payments, get_payment_status
from repository.shopping_cart_repository import get_shopping_cart_item, get_all_carts
from repository.payment_repository import get_all_payments
from repository.product_repository import Product, add_product, get_all_products, get_product_by_id
from repository.shopping_cart_repository import ShoppingCart
from repository.product_photos_repository import ProductPhoto


class Product_Services():
    # Single responsibility

    @staticmethod
    def getproducts():
        return get_all_products()

    @staticmethod
    def getproduct(product):
        return get_product_by_id(product)
