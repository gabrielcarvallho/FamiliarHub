import uuid
from django.db import transaction
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied

from apps.core.services import ServiceBase
from apps.orders.services import ProductOrderService
from apps.stock.services import StockConfigurationService

from apps.products.repositories import ProductRepository
from apps.orders.repositories import ProductOrderRepository
from apps.orders.repositories.order_repository import OrderRepository
from apps.orders.repositories import StatusRepository, PaymentRepository
from apps.customers.repositories import CustomerRepository, AddressRepository


class OrderService(metaclass=ServiceBase):
    def __init__(
            self, 
            repository=OrderRepository(),
            status_repository=StatusRepository(),
            payment_repository=PaymentRepository(),
            customer_repository=CustomerRepository(),
            address_repository=AddressRepository(),
            product_repository=ProductRepository(),
            product_order_repository=ProductOrderRepository(),

            product_order_service=ProductOrderService(),
            stock_configuration_service=StockConfigurationService()
        ):

        self.__repository = repository
        self.__status_repository = status_repository
        self.__payment_repository = payment_repository
        self.__customer_repository = customer_repository
        self.__address_repository = address_repository
        self.__product_repository = product_repository
        self.__product_order_repository = product_order_repository

        self.__product_order_service = product_order_service
        self.__stock_configuration_service = stock_configuration_service

    def get_order(self, order_id):
        if not self.__repository.exists_by_id(order_id):
            raise NotFound('Order not found.')
        
        return self.__repository.get_by_id(order_id)
    
    def get_orders_by_user(self, user):
        if not user.groups.filter(name='delivery_person'):
            return self.__repository.filter(
                created_by_id=user.id,
                order_status__identifier=0
            )
        else:
            return self.__repository.filter(
                order_status__identifier=2
            )
    
    def get_all_orders(self):
        return self.__repository.get_all()

    @transaction.atomic
    def create_order(self, request, **data):
        customer_id = data.get('customer_id')
        status_id = data.get('order_status_id')
        payment_id = data.get('payment_method_id')
        delivery_method = data.get('delivery_method')
        delivery_address_id = data.get('delivery_address_id', None)
        new_delivery_address = data.pop('delivery_address', None)
        products_data = data.pop('products')

        if not self.__customer_repository.exists_by_id(customer_id):
            raise NotFound('Customer not found.')
        
        if not self.__status_repository.exists_by_id(status_id):
            raise NotFound('Status not found.')
        
        if not self.__payment_repository.exists_by_id(payment_id):
            raise NotFound('Payment method not found.')

        if delivery_method == 'ENTREGA':
            if delivery_address_id:
                if not self.__address_repository.exists_by_id(delivery_address_id):
                    raise NotFound('Delivery address not found.')
                
                address = self.__address_repository.get_by_id(delivery_address_id)
                if address.customer.id != customer_id:
                    raise ValidationError('Delivery address provided does not belong to the customer.')
            else:
                new_delivery_address['customer_id'] = customer_id
                address = self.__address_repository.create(new_delivery_address)

                data['delivery_address_id'] = address.id
        
        data['created_by_id'] = request.user.id

        product_ids = list(set([uuid.UUID(str(item['product_id'])) for item in products_data]))
        products = {p.id: p for p in self.__product_repository.filter_by_id(product_ids)}

        if len(products) != len(set(product_ids)):
            missing_ids = set(product_ids) - set(products.keys())
            raise ValidationError(f"Products not found: {', '.join(str(pid) for pid in missing_ids)}")
        
        inactive_products = [p.name for p in products.values() if not p.is_active]
        if inactive_products:
            raise ValidationError(f"Inactive products cannot be ordered: {', '.join(inactive_products)}")
        
        self.__stock_configuration_service.validate_current_stock(products, products_data)
        order = self.__repository.create(data)

        for product in products_data:
            product['order_id'] = order.id

            if not product.get('sale_price'):
                product['sale_price'] = products[product['product_id']].price

        self.__product_order_repository.bulk_create(products_data)
        self.__stock_configuration_service.consume_stock(products, products_data)
    
    @transaction.atomic
    def update_order(self, obj, **data):
        customer_id = data.get('customer_id', None)
        if customer_id:
            if not self.__customer_repository.exists_by_id(customer_id):
                raise NotFound('Customer not found.')
        
        if 'order_status_id' in data:
            status_id = data.get('order_status_id', None)
            if status_id:
                if not self.__status_repository.exists_by_id(status_id):
                    raise NotFound('Status not found.')
        
        if 'payment_method_id' in data:
            payment_id = data.get('payment_method_id', None)
            if payment_id:
                if not self.__payment_repository.exists_by_id(payment_id):
                    raise NotFound('Payment method not found.')
        
        if 'delivery_address_id' in data:
            delivery_address_id = data.get('delivery_address_id', None)
            if delivery_address_id:
                if not self.__address_repository.exists_by_id(delivery_address_id):
                    raise NotFound('Delivery address not found.')
                
                address = self.__address_repository.get_by_id(delivery_address_id)
                if address.customer.id != customer_id:
                    raise ValidationError('Delivery address provided does not belong to the customer.')
        elif 'delivery_address' in data:
            new_delivery_address = data.pop('delivery_address')

            new_delivery_address['customer_id'] = data.get('customer_id') if customer_id else obj.customer.id
            address = self.__address_repository.create(new_delivery_address)

            data['delivery_address_id'] = address.id
        
        if 'is_delivered' in data:
            if obj.order_status.identifier != 2:
                raise ValidationError('Cannot mark an order as delivered.')
        
        products_data = data.get('products', None)
        if products_data:
            product_ids = list(set([uuid.UUID(str(item['product_id'])) for item in products_data]))
            products = {p.id: p for p in self.__product_repository.filter_by_id(product_ids)}
        
            if len(products) != len(set(product_ids)):
                missing_ids = set(product_ids) - set(products.keys())
                raise ValidationError(f"Products not found: {', '.join(str(pid) for pid in missing_ids)}")
            
            inactive_products = [p.name for p in products.values() if not p.is_active]
            if inactive_products:
                raise ValidationError(f"Inactive products cannot be ordered: {', '.join(inactive_products)}")
            
            self._reconcile_stock_for_order_update(obj, products, products_data)
            self.__product_order_service.update_products(obj.id, products, products_data)

        for attr, value in data.items():
            setattr(obj, attr, value)

        self.__repository.save(obj)
    
    def finish_work(self, user):
        if not user.groups.filter(name='sales_person') and not user.is_admin:
            raise PermissionDenied('You do not have permission to access this resource.')
        
        orders = self.__repository.filter(
            created_by_id=user.id,
            order_status__sequence_order=0
        )
        new_status = self.__status_repository.get_by_sequence_order(sequence_order=1)

        self.__repository.update(orders, order_status=new_status.id)
    
    def delete_order(self, order_id):
        if not self.__repository.exists_by_id(order_id):
            raise NotFound('Order not found.')

        self.__repository.delete(order_id)
    
    def _reconcile_stock_for_order_update(self, order, products, products_data):
        current_items = {item.product_id: item.quantity for item in order.product_items.all()}
        new_items = {item['product_id']: item['quantity'] for item in products_data}

        affected_product_ids = set(current_items.keys()) | set(new_items.keys())

        deltas = {}
        for product_id in affected_product_ids:
            old_qty = current_items.get(product_id, 0)
            new_qty = new_items.get(product_id, 0)

            delta = new_qty - old_qty
            deltas[product_id] = delta

        insufficient_stock = []
        products_without_config = []
        for product_id, delta in deltas.items():
            if delta > 0:
                product = products[product_id]

                if not hasattr(product, 'stock_settings') or not product.stock_settings:
                    products_without_config.append(product.name)
                    continue
                
                if product.stock_settings.current_stock < delta:
                    insufficient_stock.append({
                        'product_name': product.name,
                        'requested': delta,
                        'available': product.stock_settings.current_stock
                    })
                
        if products_without_config:
            raise ValidationError(
                f"Products without valid stock configuration: {', '.join(products_without_config)}"
            )

        if insufficient_stock:
            error_details = [
                f"{item['product_name']}: requested {item['requested']}, available {item['available']}"
                for item in insufficient_stock
            ]
            
            raise ValidationError(f"Insufficient stock for products: {'; '.join(error_details)}")
        
        for product_id, delta in deltas.items():
            if delta == 0:
                continue
            
            product = products[product_id]
            stock_config = product.stock_settings
            
            if delta > 0:
                stock_config.current_stock -= delta
            else:
                stock_config.current_stock += abs(delta)
            
            stock_config.save(update_fields=['current_stock', 'updated_at'])