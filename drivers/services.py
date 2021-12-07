from drivers.models import Driver
from datetime import datetime


class DriverService():

    @staticmethod
    def create_driver(first_name, last_name, created_at=None, updated_at=None):
        if created_at and updated_at and updated_at < created_at:
            raise ValueError("updated_at can't be earlier, then created_at")
        if not created_at:
            created_at = datetime.now()
        if not updated_at:
            updated_at = datetime.now()
        driver = Driver.objects.create(first_name=first_name, last_name=last_name,
                                       created_at=created_at, updated_at=updated_at)
        return driver

    @staticmethod
    def update_driver(pk, first_name=None, last_name=None, created_at=None, updated_at=None):
        updated_driver = Driver.objects.get(pk=pk)
        if not updated_driver:
            raise ValueError("Not Found")
        if first_name:
            updated_driver.first_name = first_name
        if last_name:
            updated_driver.last_name = last_name
        if created_at and updated_at and updated_at < created_at:
            raise ValueError("updated_at can't be earlier, then created_at")
        if created_at:
            updated_driver.created_at = created_at
        if updated_at:
            updated_driver.updated_at = updated_at
        else:
            updated_driver.updated_at = datetime.now()
        updated_driver.save()
        return updated_driver

    @staticmethod
    def filter_by_creation_date(queryset, created_after=None, created_before=None):
        # if created_after and updated_at and updated_at < created_at:
        #     raise ValueError("updated_at can't be earlier, then created_at")
        if created_after:
            queryset = queryset.filter(created_at__gte=created_after)
        if created_before:
            queryset = queryset.filter(created_at__lte=created_before)
        return queryset
