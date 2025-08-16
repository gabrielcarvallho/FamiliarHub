from django.db import models


class ProductionStatus(models.IntegerChoices):
    PLANNED = 0
    INPROGRESS = 1
    COMPLETED = 2