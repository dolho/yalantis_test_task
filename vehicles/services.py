import re
from datetime import datetime
from vehicles.models import Vehicle
from drivers.models import Driver
from django.db.utils import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404

class VehicleService():

    @staticmethod
    def get_vehicles_with_drivers():
        vehicles = Vehicle.objects.all() #select_related('Driver')
        return vehicles

    # @staticmethod
    # def get_vehicles():
    #     vehicles = Vehicle.objects.all() #select_related('Driver')
    #     return vehicles

    @staticmethod
    def validate_plate_number(plate_number: str) -> bool:
        if len(plate_number) != 10:
            return False
        result = re.match("[A-Z]{2} [0-9]{4} [A-Z]{2}", plate_number)
        if result:
            return True
        return False

    @staticmethod
    def example_of_plate_number():
        return "AA 1234 OO"

    @staticmethod
    def create_vehicle(make, model, plate_number, driver_id=None, created_at=None, updated_at=None):
        if created_at and updated_at and created_at > updated_at:
            raise ValueError("updated_at can't be earlier then created_at")
        if not created_at:
            created_at = datetime.now()
        if not updated_at:
            updated_at = created_at
        try:
            if driver_id:
                driver = Driver.objects.get(pk=driver_id)
                vehicle = Vehicle.objects.create(make=make, model=model, plate_number=plate_number, driver_id=driver,
                                                 created_at=created_at, updated_at=updated_at)
            else:
                vehicle = Vehicle.objects.create(make=make, model=model, plate_number=plate_number,
                                                 created_at=created_at, updated_at=updated_at)
        except IntegrityError as e:
            raise ValueError(e)
        return vehicle

    @staticmethod
    def update(pk, make=None, model=None, plate_number=None, created_at=None, updated_at=None):
        if created_at and updated_at and updated_at < created_at:
            raise ValueError("updated_at can't be earlier, then created_at")
        vehicle = get_object_or_404(Vehicle.objects.all(), pk=pk)
        vehicle.make = make if make else vehicle.make
        vehicle.model = model if model else vehicle.model
        vehicle.plate_number = plate_number if plate_number else plate_number
        vehicle.created_at = created_at if created_at else vehicle.created_at
        vehicle.updated_at = updated_at if updated_at else datetime.now()
        vehicle.save()
        return vehicle

    @staticmethod
    def update_instance(vehicle, make=None, model=None, plate_number=None, created_at=None, updated_at=None):
        if created_at and updated_at and updated_at < created_at:
            raise ValueError("updated_at can't be earlier, then created_at")
        vehicle.make = make if make else vehicle.make
        vehicle.model = model if model else vehicle.model
        vehicle.plate_number = plate_number if plate_number else plate_number
        vehicle.created_at = created_at if created_at else vehicle.created_at
        vehicle.updated_at = updated_at if updated_at else datetime.now()
        vehicle.save()
        return vehicle


    @staticmethod
    def set_driver(driver_id, vehicle_id):
        driver_queryset = Driver.objects.all()
        driver = get_object_or_404(driver_queryset, pk=driver_id)

        vehicle_queryset = Vehicle.objects.all()
        vehicle = get_object_or_404(vehicle_queryset, pk=vehicle_id)
        if vehicle.driver_id is not None:
            raise ValueError("Vehicle already have driver")
        vehicle.driver_id = driver
        try:
            vehicle.save()
        except IntegrityError as e:
            msg = "Driver already have vehicle"
            raise ValueError(msg)
        return vehicle

    @staticmethod
    def unset_driver(vehicle_id):
        vehicle_queryset = Vehicle.objects.all()
        vehicle = get_object_or_404(vehicle_queryset, pk=vehicle_id)
        vehicle.driver_id = None
        vehicle.save()
        return vehicle
