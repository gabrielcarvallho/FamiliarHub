from django.db import models


class CustomerType(models.TextChoices):
    PF = "PF"
    PJ = "PJ"