from rest_framework import serializers


class DateField(serializers.DateField):
    default_error_messages = {
        "invalid_day": "Delivery date cannot be on a weekend."
    }
    def to_internal_value(self, value):
        data = super().to_internal_value(value)

        if data.weekday() >= 5:
            self.fail('invalid_day')
        
        return data