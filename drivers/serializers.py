from rest_framework import serializers
from drivers.models import Driver
from drivers.services import DriverService
from datetime import datetime


class DriverSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'created_at', 'updated_at']


class DriverSerializerPost(serializers.ModelSerializer):

    def validate(self, data):
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)

        if first_name is None:
            raise serializers.ValidationError(
                'A first name is required to create driver.'
            )
        if last_name is None:
            raise serializers.ValidationError(
                'A last name is required to create driver'
            )
        return {
                'first_name': first_name.strip(),
                'last_name': last_name.strip(),
        }

    def create(self, validated_data):
        driver = DriverService.create_driver(**validated_data)

        return {
            'first_name': driver.first_name,
            'last_name': driver.last_name,
            'created_at': driver.created_at,
            'updated_at': driver.updated_at,
        }

    class Meta:
        model = Driver
        fields = ['first_name', 'last_name']


class DriverSerializerPut(serializers.ModelSerializer):

    def validate(self, data):
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)

        if first_name is None:
            raise serializers.ValidationError(
                'A first name is required to update driver.'
            )
        if last_name is None:
            raise serializers.ValidationError(
                'A last name is required to update driver'
            )
        return {
                'first_name': first_name.strip(),
                'last_name': last_name.strip(),
        }

    class Meta:
        model = Driver
        fields = ['first_name', 'last_name']


class DriverSerializerPatch(serializers.Serializer):
    first_name = serializers.CharField(required=False,default=None)
    last_name = serializers.CharField(required=False,default=None)

    def validate(self, data):

        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)

        if not (first_name or last_name):
                 raise serializers.ValidationError(
                'At least first or last name required'
            )
        return {
                'first_name': first_name.strip(),
                'last_name': last_name.strip(),
        }
