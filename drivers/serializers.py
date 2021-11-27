from django.contrib.auth.models import User, Group
from rest_framework import serializers
from drivers.models import Driver
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
                'A last name is required to log in.'
            )
        created_at = datetime.now()
        updated_at = created_at
        return {
                'first_name': first_name.strip(),
                'last_name': last_name.strip(),
                'created_at': created_at,
                'updated_at': updated_at,
        }

    def create(self, validated_data):
        driver = Driver.objects.create(**validated_data)
        return {
            'first_name': driver.first_name,
            'last_name': driver.last_name,
            'created_at': driver.created_at,
            'updated_at': driver.updated_at,
        }
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name']


