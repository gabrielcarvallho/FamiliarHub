import re
from rest_framework import serializers


def validate_cnpj(value):
    cnpj = re.sub(r'\D', '', value)

    if len(cnpj) != 14 or not cnpj.isdigit():
        raise serializers.ValidationError("CNPJ must contain 14 numeric digits.")

    if cnpj in (cnpj[0] * 14 for _ in range(10)):
        raise serializers.ValidationError("Invalid CNPJ.")

    def calculate_digit(cnpj, digit):
        weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        if digit == 1:
            weights = weights[1:]

        total = sum(int(cnpj[i]) * weights[i] for i in range(len(weights)))
        remainder = total % 11

        return '0' if remainder < 2 else str(11 - remainder)

    if cnpj[12] != calculate_digit(cnpj[:12], 1) or cnpj[13] != calculate_digit(cnpj[:13], 2):
        raise serializers.ValidationError("Invalid CNPJ.")

    return cnpj

def validate_phone(value):
    digits = re.sub(r'\D', '', value)
    if len(digits) not in [10, 11]:
        raise serializers.ValidationError("Phone number must contain 10 or 11 numeric digits.")
    
    return value

def validate_state_tax_registration(value):
    if value:
        value = value.strip()
        
        if not re.fullmatch(r'[A-Za-z0-9]{9,14}', value):
            raise serializers.ValidationError("Invalid state tax registration. Must contain 9 to 14 alphanumeric characters.")
        
    return value