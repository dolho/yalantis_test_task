"""motor_depot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from drivers.views import DriverViewSet
from vehicles.views import VehicleViewSet
from rest_framework.routers import DefaultRouter
from django.http import HttpRequest

router_drivers = routers.DefaultRouter()
router_drivers.register('driver', DriverViewSet)

router_vehicles = routers.DefaultRouter()
router_vehicles.register('vehicle', VehicleViewSet)

# For some reason technical task for set-driver endpoint is demanded to be like this  /vehicles/set_driver/<vehicle_id>/
# When it could be like this: /vehicles/vehicle/<vehicle_id>/set-driver - which is much cleaner and logical
# So that's why I wrote this terribleness
set_driver_view = VehicleViewSet.as_view({'post': 'set_driver'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drivers/', include(router_drivers.urls)),
    path('vehicles/', include(router_vehicles.urls)),
    path('vehicles/set-driver/<int:pk>', set_driver_view)
]
