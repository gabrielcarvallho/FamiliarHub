from django.db import models


class DeliveryMethod(models.TextChoices):
    PICKUP = 'RETIRADA'
    DELIVERY = 'ENTREGA'

class StatusCategory(models.IntegerChoices):
    OPERATIONAL = 1
    LOGISTIC = 2
    PAYMENT = 3
    COMPLETION = 4