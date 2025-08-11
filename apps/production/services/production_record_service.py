from datetime import datetime
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import NotFound, ValidationError

from apps.core.services import ServiceBase
from apps.production.services import ProductionItemService
from apps.production.repositories import ProductionRecordRepository


class ProductionRecordService(metaclass=ServiceBase):
    def __init__(
            self, 
            repository=ProductionRecordRepository(),
            production_item_service=ProductionItemService()
        ):

        self.__repository = repository
        self.__production_item_service = production_item_service
    
    def get_record(self, record_id):
        if not self.__repository.exists_by_id(record_id):
            raise NotFound("Production record not found.")
        
        return self.__repository.get_by_id(record_id)
    
    def get_all_records(self, start_date=None, end_date=None):
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
        return self.__repository.get_all(start_date, end_date)
    
    @transaction.atomic
    def create_record(self, request, **data):
        status = data.get('status')
        start_date = data.get('start_date')
        end_date = data.get('end_date', None)
        items = data.pop('production_items')

        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                data['start_date'] = start_date

            if end_date and isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                data['end_date'] = end_date  
        except ValueError as e:
            raise ValidationError(f"Invalid date format. Use YYYY-MM-DD format: {str(e)}")

        if status == 0:
            if start_date < timezone.now().date():
                raise ValidationError("Start date cannot be less than the current date when the status is 'PLANNED'")
        elif status == 2:
            if not end_date:
                raise ValidationError("End date is required when status is 'COMPLETED'")
            
            if end_date < start_date:
                raise ValidationError("End date must be greater than start date")
        
        data['created_by_id'] = request.user.id

        production_record = self.__repository.create(data)
        self.__production_item_service.create_items(production_record, items)

        if status == 2:
            self.__production_item_service.update_current_stock(production_record)
    
    @transaction.atomic
    def update_record(self, obj, **data):
        status = data.get('status')
        start_date = data.get('start_date')
        end_date = data.get('end_date', None)
        items = data.pop('production_items')

        if obj.status == 2:
            raise ValidationError("Cannot change the record status once it is completed.")

        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                data['start_date'] = start_date

            if end_date and isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                data['end_date'] = end_date 
        except ValueError as e:
            raise ValidationError(f"Invalid date format. Use YYYY-MM-DD format: {str(e)}")

        if status == 0:
            if start_date < timezone.now().date():
                raise ValidationError("Start date cannot be less than the current date when the status is 'PLANNED'")
        elif status == 2:
            if not end_date:
                raise ValidationError("End date is required when status is 'COMPLETED'")
            
            if end_date <= start_date:
                raise ValidationError("End date must be greater than start date")
        
        for attr, value in data.items():
            setattr(obj, attr, value)

        self.__repository.save(obj)
        self.__production_item_service.update_production_items(obj, items)

        if status == 2:
            self.__production_item_service.update_current_stock(obj)
    
    def delete_record(self, record_id):
        if not self.__repository.exists_by_id(record_id):
            raise NotFound("Production record not found.")
        
        self.__repository.delete(record_id)