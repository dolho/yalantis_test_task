from django.shortcuts import render
from rest_framework import viewsets
from vehicles.models import Vehicle
from vehicles import serializers
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
from vehicles.services import VehicleService
from django.shortcuts import get_object_or_404
from drivers.models import Driver
from django.db.models import Q
# Create your views here.


class VehicleViewSet(viewsets.ModelViewSet):
    """
    Drivers
    """
    basename = "driver"
    queryset = Vehicle.objects.all()
    serializer_class = serializers.VehicleSerializerList
    serializer_action_classes = {
        'create': serializers.VehicleSerializerPost,
        'list': serializers.VehicleSerializerList,
        'retrieve': serializers.VehicleSerializerList,
        'set_driver': serializers.VehicleSerializerSetDriver,
        'update': serializers.VehicleSerializerPut,
        'partial_update': serializers.VehicleSerializerPatch
        # 'partial_update': serializers.VehicleSerializerPatch
    }
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        with_drivers = self.request.query_params.get('with_drivers')
        if with_drivers:
            if with_drivers == 'yes':
                vehicles = Vehicle.objects.filter(~Q(driver_id=None))
                page = self.paginate_queryset(vehicles)

                serializer = self.get_serializer_class()(page, many=True)
                return self.get_paginated_response(serializer.data)
            elif with_drivers == 'no':
                vehicles = Vehicle.objects.filter(driver_id=None)
                page = self.paginate_queryset(vehicles)
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                vehicles = Vehicle.objects.all()
                page = self.paginate_queryset(vehicles)
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        else:
            vehicles = Vehicle.objects.all()
            page = self.paginate_queryset(vehicles)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Vehicle.objects.all()
        vehicle = get_object_or_404(queryset, pk=pk)
        return Response(self.get_serializer_class()(vehicle, depth=0).data)

    def set_driver(self, request, pk=None):
        driver_id = self.get_serializer_class().validate(self, self.request.data)['driver_id']
        # driver_id = self.request.data['driver_id']
        if driver_id is None:
            vehicle = VehicleService.unset_driver(pk)
            return Response(serializers.VehicleSerializerSetDriver(vehicle).data)
        try:
            vehicle = VehicleService.set_driver(driver_id, pk)
        except ValueError as e:
            exc = APIException(detail=e, code=status.HTTP_409_CONFLICT)
            exc.status_code = 409
            raise exc
        return Response(self.get_serializer_class()(vehicle).data)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(VehicleViewSet, self).get_serializer_class()