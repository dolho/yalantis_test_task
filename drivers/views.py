from rest_framework import viewsets
from rest_framework import permissions
from drivers import serializers
from drivers.models import Driver
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from django_filters.rest_framework import DjangoFilterBackend
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
        'update': serializers.DriverSerializerPost
    }
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['created_at']

    def update(self, request, pk=None):
        updated_driver = Driver.objects.get(pk=pk)
        if not updated_driver:
            raise NotFound('There is no driver with such pk')

        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        if not first_name and last_name:
            raise ValidationError("No firstname given")
        if not last_name:
            raise ValidationError("No lastname given")
        updated_driver.first_name = first_name
        updated_driver.last_name = last_name
        updated_driver.updated_at = datetime.now()
        updated_driver.save()
        return Response(self.serializer_class(updated_driver).data)

    def partial_update(self, request, pk=None):
        updated_driver = Driver.objects.get(pk=pk)
        if not updated_driver:
            raise NotFound('There is no driver with such pk')
        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        if first_name:
            updated_driver.first_name = first_name
        if last_name:
            updated_driver.last_name = last_name
        updated_driver.updated_at = datetime.now()
        updated_driver.save()
        return Response(self.serializer_class(updated_driver).data)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `created_at__gte` query parameter in the URL.
        """
        queryset = Driver.objects.all()
        created_after = self.request.query_params.get('created_at__gte')
        created_before = self.request.query_params.get('created_at__lte')
        if created_after is not None:
            created_after = datetime.fromisoformat(str(created_after))
            queryset = queryset.filter(created_at__gte=created_after)
        if created_before is not None:
            created_before = datetime.fromisoformat(str(created_before))
            queryset = queryset.filter(created_at__lte=created_before)
        return queryset

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(DriverViewSet, self).get_serializer_class()


