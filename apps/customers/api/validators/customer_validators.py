import re
from rest_framework.validators import ValidationError


class CustomerValidator:
    @staticmethod
    def clean_document(document):
        return re.sub(r'[^0-9]', '', document)
    
    @staticmethod
    def validate_cpf(cpf):
        cpf = re.sub(r'[^0-9]', '', cpf)
        
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        
        for i in range(9, 11):
            value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != int(cpf[i]):
                return False
            
        return True
    
    @staticmethod
    def validate_cnpj(cnpj):
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False
        
        sequence = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        
        for i in range(2):
            value = sum(int(cnpj[idx]) * sequence[idx] for idx in range(len(sequence)))
            digit = 11 - (value % 11)
            if digit >= 10:
                digit = 0
            if digit != int(cnpj[12 + i]):
                return False
            sequence.insert(0, 6)
        
        return True
    
    @staticmethod
    def validate_document_by_type(customer_type, document):
        clean_doc = CustomerValidator.clean_document(document)

        if customer_type == 'PF':
            if not CustomerValidator.validate_cpf(clean_doc):
                raise ValidationError("Invalid CPF format")
        elif customer_type == 'PJ':
            if not CustomerValidator.validate_cnpj(clean_doc):
                raise ValidationError("Invalid CNPJ format")
        else:
            raise ValidationError("Invalid customer type")
        
        return clean_doc