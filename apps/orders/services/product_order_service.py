import uuid
from rest_framework.exceptions import ValidationError

from apps.core.services import ServiceBase
from apps.orders.repositories import ProductOrderRepository


class ProductOrderService(metaclass=ServiceBase):
    def __init__(
            self,
            repository=ProductOrderRepository()
        ):
        
        self.__repository = repository
    
    def update_products(self, order_id, products_obj, products_data):
        products_to_remove = []
        products_to_keep = []

        for p in products_data:
            product_id = uuid.UUID(str(p['product_id']))
            quantity = p.get('quantity', 0)

            if quantity == 0:
                products_to_remove.append(product_id)
            else:
                products_to_keep.append({
                    'product_id': product_id,
                    'quantity': quantity,
                    'sale_price': p.get('sale_price'),
                })

        if products_to_remove:
            self.__repository.delete(order_id, products_to_remove)

        if not products_to_keep:
            return

        current_products = {
            p.product_id: p for p in self.__repository.filter_by_order_id(order_id)
        }

        to_update = []
        to_create = []

        for p in products_to_keep:
            product_id = p['product_id']
            quantity = p['quantity']
            sale_price = p['sale_price'] if p['sale_price'] is not None else products_obj[product_id].price

            if product_id in current_products:
                current = current_products[product_id]

                if current.quantity != quantity or current.sale_price != sale_price:
                    current.quantity = quantity
                    current.sale_price = sale_price

                    to_update.append(current)
            else:
                to_create.append({
                    'order_id': order_id,
                    'product_id': product_id,
                    'quantity': quantity,
                    'sale_price': sale_price,
                })

        if to_update:
            self.__repository.bulk_update(to_update, ['quantity', 'sale_price'])

        if to_create:
            self.__repository.bulk_create(to_create)
    
    def validate_current_stock(self, obj, products_data):
        insufficient_stock = []
    
        for item in products_data:
            product_id = item['product_id']
            quantity = item['quantity']
            product = obj[product_id]
            
            if product.current_stock < quantity:
                insufficient_stock.append({
                    'product_name': product.name,
                    'requested': quantity,
                    'available': product.current_stock
                })
        
        if insufficient_stock:
            error_details = [
                f"{item['product_name']}: requested {item['requested']}, available {item['available']}"
                for item in insufficient_stock
            ]

            raise ValidationError(f"Insufficient stock for products: {'; '.join(error_details)}")