from django.db import models
from drivers.models import Driver

# Create your models here.


class Vehicle(models.Model):
    driver_id = models.OneToOneField(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __int__(self):
        return self.id