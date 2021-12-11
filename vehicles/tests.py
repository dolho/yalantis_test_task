from django.test import TestCase
from .services import VehicleService
from drivers.services import DriverService
from django.urls import reverse
import json
# Create your tests here.



class DriverViewTests(TestCase):

    def setUp(self):
        DriverService.create_driver("First", "Driver", '2021-12-04 19:02:16.192857', '2021-12-04 19:02:16.192857', )
        DriverService.create_driver("Second", "Driver", '2021-12-04 19:02:16.192857', '2021-12-04 19:02:16.192857', )
        VehicleService.create_vehicle("FirstVehicle", "Model", "AA 1234 BB", 1,
                                      '2021-12-04 19:02:16.192857', '2021-12-04 19:02:16.192857',)
        VehicleService.create_vehicle("SecondVehicle", "Model", "BB 1234 CC", None,
                                      '2021-09-04 19:02:16.192857', '2021-12-04 19:02:16.192857')
        VehicleService.create_vehicle("ThirdVehicle", "Model", "CC 1234 DD", None,
                                      '2021-06-04 19:02:16.192857', '2021-12-04 19:02:16.192857')

    def test_list_works(self):
        response = self.client.get(reverse("vehicle-list"))  # reverse('driver:index')
        self.assertEqual(response.headers["Content-Type"], "application/json")
        for vehicle in json.loads(response.content)["results"]:
            self.assertEqual(list(vehicle.keys()), ['id', 'driver_id', 'make', 'model', 'plate_number',
                                                    'created_at', 'updated_at'])
            self.assertIn(vehicle['driver_id'], [1, None])

    def test_list_with_drivers(self):
        response = self.client.get(reverse("vehicle-list"), {'with_drivers': 'yes'})
        self.assertEqual(response.headers["Content-Type"], "application/json")
        for vehicle in json.loads(response.content)["results"]:
            self.assertEqual(vehicle['id'], 1)
            self.assertEqual(vehicle['driver_id'], 1)

    def test_list_without_drivers(self):
        response = self.client.get(reverse("vehicle-list"), {'with_drivers': 'no'})
        self.assertEqual(response.headers["Content-Type"], "application/json")
        vehicle = json.loads(response.content)
        self.assertEqual(vehicle["count"], 2)
        self.assertEqual(vehicle["results"][0]['driver_id'], None)

    def test_list_incorrect_drivers(self):
        response = self.client.get(reverse("vehicle-list"), {'with_drivers': 'incorrec_values'})
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content["count"], 3)
        for vehicle in content["results"]:
            self.assertIn(vehicle['driver_id'], [1, None])

    def test_get_vehicle_data(self):
        response = self.client.get(reverse("vehicle-detail", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['driver_id'], 1)

    def test_post_vehicle(self):
        response = self.client.post(reverse("vehicle-list"), {'make': 'FourthVehicle',
                                                              'model': 'Model',
                                                              'plate_number': 'EE 1234 FF'})
        self.assertEqual(response.status_code, 201, msg=json.loads(response.content))
        self.assertEqual(json.loads(response.content)['driver_id'], None)

    def test_post_vehicle_with_driver_which_already_has_vehicle(self):
        response = self.client.post(reverse("vehicle-list"), {'make': 'FourthVehicle',
                                                              'driver_id': 1,
                                                              'model': 'Model',
                                                              'plate_number': 'EE 1234 FF'})
        self.assertEqual(response.status_code, 409, msg=json.loads(response.content))

    def test_post_vehicle_with_driver(self):
        response = self.client.post(reverse("vehicle-list"), {'make': 'FourthVehicle',
                                                              'driver_id': 2,
                                                              'model': 'Model',
                                                              'plate_number': 'EE 1234 FF'})
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEqual(content['driver_id'], 2)

    def test_delete_vehicle(self):
        response = self.client.post(reverse("vehicle-list"), {'make': 'FourthVehicle',
                                                              'driver_id': 2,
                                                              'model': 'Model',
                                                              'plate_number': 'EE 1234 FF'})
        self.assertEqual(response.status_code, 201)
        vehicle = json.loads(response.content)
        response = self.client.delete(reverse("vehicle-detail", kwargs={'pk': vehicle['id']}), content_type="application/json")
        self.assertEqual(response.status_code, 204)
        response = self.client.get(reverse("vehicle-detail", kwargs={'pk': vehicle['id']}))
        self.assertEqual(response.status_code, 404)

    def test_set_driver(self):
        response = self.client.post(reverse("set-driver", kwargs={'pk': 2}), {'driver_id': 2})
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200, msg=content)
        self.assertEqual(content['driver_id'], 2, msg=content)
        self.assertEqual(content['id'], 2, msg=content)

    def test_unset_driver(self):
        response = self.client.post(reverse("set-driver", kwargs={'pk': 1}), {'driver_id': None},
                                    content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200, msg=content)
        self.assertEqual(content['driver_id'], None, msg=content)
        self.assertEqual(content['id'], 1, msg=content)

    def test_put(self):
        response = self.client.put(reverse("vehicle-detail", kwargs={'pk': 3}),
                                    {'make': 'ChangedVehicle',
                                    'plate_number': 'EE 1234 FF'},
                                    content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400, msg=content)

        response = self.client.put(reverse("vehicle-detail", kwargs={'pk': 3}),
                                   {'make': 'ChangedVehicle',
                                    'model': 'ChangedModel',
                                    'plate_number': 'EE 1234 FF'},
                                   content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200, msg=content)
        self.assertEqual(content['model'], 'ChangedModel', msg=content)
        self.assertEqual(content['make'], 'ChangedVehicle', msg=content)

    def test_patch(self):
        response = self.client.patch(reverse("vehicle-detail", kwargs={'pk': 3}),
                                   {'make': 'ChangedVehicle',
                                    'plate_number': 'EE 8888 FF'},
                                   content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200, msg=content)
        self.assertEqual(content['model'], 'Model', msg=content)
        self.assertEqual(content['make'], 'ChangedVehicle', msg=content)