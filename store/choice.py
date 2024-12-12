from django.db import models


class UserRoleChoice(models.TextChoices):
    ULTRA_ADMIN = 'ultraAdmin'
    SUPER_ADMIN = 'superAdmin'
    ADMIN = 'admin'
    MANAGER = 'manager'
    DISTRIBUTER = 'distributer'
    RETAILER = 'retailer'


    