from vehicles.models import Vehicle
from vehicles.services import VehicleService
from rest_framework import serializers



class VehicleSerializerList(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ['id', 'driver_id', 'make', 'model', 'plate_number', 'created_at', 'updated_at']
        depth = 0

    def __init__(self, *args, **kwargs):
        depth = kwargs.pop("depth", None)

        if depth is not None:
            if not (depth_type := type(depth) is int):
                raise TypeError(f'Depth should be an integer. Instead it is {depth_type}')
            self.Meta.depth = depth
        else:
            self.Meta.depth = 0

        super(VehicleSerializerList, self).__init__(*args, **kwargs)


class VehicleSerializerPost(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False, allow_null=True, default=None)
    # driver_id = serializers.IntegerField(required=False, allow_null=True, default=None)
    # make = serializers.CharField(max_length=100)
    # model = serializers.CharField(max_length=100)
    # plate_number = serializers.CharField(max_length=10)
    driver_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_plate_number(self, plate_number):
        if not VehicleService.validate_plate_number(plate_number):
            raise serializers.ValidationError(
                f'Incorrect plate number. Example of correct plate number: {VehicleService.example_of_plate_number()}'
            )
        return plate_number

    # def validate_driver_id(self, driver_id):
    #     return driver_id

    class Meta:
        model = Vehicle
        fields = ['id', 'driver_id', 'make', 'model', 'plate_number', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at')
        # extra_kwargs = {
        #     'driver_id': {'required': False, 'allow_null': True, 'default': None},
        # }
        depth = 0


    def create(self, validated_data):
        try:
            vehicle = VehicleService.create_vehicle(**validated_data)
        except ValueError as e:
            err = serializers.ValidationError(e)
            err.status_code = 409
            raise err
            # return Response({'ValidationError': }, status=status.HTTP_409_CONFLICT)
        return {
            'id': vehicle.id,
            'driver_id': vehicle.driver_id.id if vehicle.driver_id else vehicle.driver_id,
            'make': vehicle.make,
            'model': vehicle.model,
            'plate_number': vehicle.plate_number,
            'created_at': vehicle.created_at,
            'updated_at': vehicle.updated_at,
        }


class VehicleSerializerSetDriver(serializers.ModelSerializer):
    driver_id = serializers.IntegerField(required=True, allow_null=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'driver_id', 'make', 'model', 'plate_number', 'created_at', 'updated_at']
        read_only_fields = ('id', 'make', 'model', 'plate_number', 'created_at', 'updated_at')
        depth = 0

    def validate(self, data):
        try:
            driver_id = data['driver_id']
        except KeyError:
            raise serializers.ValidationError({"driver_id": "This field is required"})
        return {
            "driver_id": driver_id
        }


class VehicleSerializerPut(serializers.ModelSerializer):

    def validate_plate_number(self, plate_number):
        if not VehicleService.validate_plate_number(plate_number):
            raise serializers.ValidationError(
                f'Incorrect plate number. Example of correct plate number: {VehicleService.example_of_plate_number()}'
            )
        return plate_number

    def update(self, instance, validated_data):
        VehicleService.update_instance(instance, **validated_data)
        return instance

    class Meta:
        model = Vehicle
        fields = ['id', 'driver_id', 'make', 'model', 'plate_number', 'created_at', 'updated_at']
        read_only_fields = ('id', 'driver_id', 'created_at', 'updated_at')


class VehicleSerializerPatch(serializers.ModelSerializer):

    def validate_plate_number(self, plate_number):
        if not VehicleService.validate_plate_number(plate_number):
            raise serializers.ValidationError(
                f'Incorrect plate number. Example of correct plate number: {VehicleService.example_of_plate_number()}'
            )
        return plate_number

    def update(self, instance, validated_data):
        VehicleService.update_instance(instance, **validated_data)
        return instance

    class Meta:
        model = Vehicle
        fields = ['id', 'driver_id', 'make', 'model', 'plate_number', 'created_at', 'updated_at']
        read_only_fields = ('id', 'driver_id', 'created_at', 'updated_at')
