from rest_framework import viewsets
from rest_framework import permissions
from drivers import serializers
from drivers.models import Driver
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from drivers.services import DriverService
from datetime import datetime
import json

# Create your views here.


class DriverViewSet(viewsets.ModelViewSet):
    """
    Drivers
    """
    basename = "driver"
    queryset = Driver.objects.all()
    serializer_class = serializers.DriverSerializerList
    serializer_action_classes = {
        'create': serializers.DriverSerializerPost,
        'update': serializers.DriverSerializerPut,
        'partial_update': serializers.DriverSerializerPatch
    }
    permission_classes = [permissions.AllowAny]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['created_at']
    def list(self, request, *args, **kwargs):
        created_after = self.request.query_params.get('created_at__gte')
        created_before = self.request.query_params.get('created_at__lte')
        try:
            if created_after is not None:
                created_after = datetime.strptime(str(created_after), "%d-%m-%Y")
            if created_before is not None:
                created_before = datetime.strptime(str(created_before), "%d-%m-%Y")
        except ValueError:
            return Response("Given date doesn't match format day-month-year.", status=status.HTTP_400_BAD_REQUEST)
        vehicles = DriverService.filter_by_creation_date(self.get_queryset(), created_after, created_before)
        page = self.paginate_queryset(vehicles)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def update(self, request, pk=None):
        validated_data = self.serializer_action_classes[self.action]().validate(request.data)
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        try:
            updated_driver = DriverService.update_driver(pk, first_name, last_name)
        except ValueError:
            raise NotFound('There is no driver with such pk')
        return Response(self.serializer_class(updated_driver).data)

    def partial_update(self, request, pk=None):
        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        try:
            updated_driver = DriverService.update_driver(pk, first_name, last_name)
        except ValueError:
            raise NotFound('There is no driver with such pk')
        return Response(self.serializer_class(updated_driver).data)

    # def get_queryset(self):
    #     queryset = Driver.objects.all()
    #     created_after = self.request.query_params.get('created_at__gte')
    #     created_before = self.request.query_params.get('created_at__lte')
    #     try:
    #         if created_after is not None:
    #             created_after = datetime.strptime(str(created_after), "%d-%m-%Y")
    #         if created_before is not None:
    #             created_before = datetime.strptime(str(created_before), "%d-%m-%Y")
    #     except ValueError:
    #         # return Response("Given date doesn't match format day-month-year.", status=status.HTTP_400_BAD_REQUEST)
    #         # raise ValidationError("Given date doesn't match format day-month-year.")
    #     if created_after or created_before:
    #         queryset = DriverService.filter_by_creation_date(self.queryset, created_after, created_before)
    #     return queryset

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(DriverViewSet, self).get_serializer_class()


