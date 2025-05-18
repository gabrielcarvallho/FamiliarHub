import re
from rest_framework import serializers


class CNPJField(serializers.CharField):
    default_error_messages = {
        "invalid_format": "Invalid CNPJ. Must contain 14 numeric digits.",
        "invalid": "Invalid CNPJ.",
    }

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        field = re.sub(r'\D', '', data)

        if len(field) != 14 or not field.isdigit():
            self.fail('invalid_format')

        if field in (field[0] * 14 for _ in range(10)):
            raise self.fail('invalid')

        def calculate_digit(field, digit):
            weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            if digit == 1:
                weights = weights[1:]

            total = sum(int(field[i]) * weights[i] for i in range(len(weights)))
            remainder = total % 11

            return '0' if remainder < 2 else str(11 - remainder)

        if field[12] != calculate_digit(field[:12], 1) or field[13] != calculate_digit(field[:13], 2):
            self.fail('invalid')

        return field

class PhoneNumberField(serializers.CharField):
    default_error_messages = {
        "invalid_format": "Invalid phone number. Must contain 10 or 11 numeric digits."
    }

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        field = re.sub(r'\D', '', data)

        if len(field) not in [10, 11]:
            self.fail('invalid_format')
        
        return field

class StateTaxField(serializers.CharField):
    default_error_messages = {
        "invalid_format": "Invalid state tax registration. Must contain 9 to 14 alphanumeric characters."
    }

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data:
            field = data.strip()

            if not re.fullmatch(r'[A-Za-z0-9]{9,14}', data):
                self.fail('invalid_format')
            
            return field

class CEPField(serializers.CharField):
    default_error_messages = {
        "invalid_format": "Invalid CEP. Must contain 8 digits."
    }

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        field = re.sub(r'\D', '', data)

        if not len(field) == 8:
            self.fail('invalid_format')

        return field