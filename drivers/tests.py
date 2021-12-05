from django.test import TestCase
from .services import DriverService
from django.urls import reverse
import json
# Create your tests here.


class DriverViewTests(TestCase):

    def setUp(self):
        DriverService.create_driver("First", "Driver", '2021-12-04 19:02:16.192857', '2021-12-04 19:02:16.192857',)
        DriverService.create_driver("Second", "Driver", '2021-09-04 19:02:16.192857', '2021-12-04 19:02:16.192857')
        DriverService.create_driver("Third", "Driver", '2021-06-04 19:02:16.192857', '2021-12-04 19:02:16.192857')

    def test_that_all_drivers_appear_in_response(self):

        response = self.client.get(reverse("driver-list")) # reverse('driver:index')
        self.assertEqual(response.headers["Content-Type"], "application/json")
        for driver in json.loads(response.content)["results"]:
            self.assertEqual(list(driver.keys()), ['id', 'first_name', 'last_name', 'created_at', 'updated_at'])

    def test_that_created_at__gte_works(self):
        response = self.client.get(reverse("driver-list"), {'created_at__gte': '10-11-2021'})
        for driver in json.loads(response.content)["results"]:
            self.assertEqual(driver['first_name'], "First")

    def test_that_created_at__lte_works(self):
        response = self.client.get(reverse("driver-list"), {'created_at__lte': '10-11-2021'})
        for driver in json.loads(response.content)["results"]:
            self.assertIn(driver['first_name'], ["Second", "Third"])

    def test_that_created_at__gte_and_lte_works(self):
        response = self.client.get(reverse("driver-list"), {'created_at__lte': '10-11-2021',
                                                            'created_at__gte': '10-08-2021'})
        for driver in json.loads(response.content)["results"]:
            self.assertEqual(driver['first_name'], "Second")

    def test_that_get_driver_by_id_works(self):
        # print(resolve('/drivers/driver/2/'))
        response = self.client.get(reverse("driver-detail",  args=[2]))
        driver = json.loads(response.content)
        self.assertEqual(driver['first_name'], "Second")

    def test_that_post_driver_works(self):
        # print(resolve('/drivers/driver/'))
        response = self.client.post(reverse("driver-list"), data={"first_name": "New",
                                                                   "last_name": "Driver"})
        self.assertEqual(response.status_code, 201)
        driver = json.loads(response.content)
        self.assertEqual(driver['first_name'], "New")

    def test_that_put_requires_all_fields(self):
        response = self.client.put(reverse("driver-detail", args=[3]), data={"first_name": "Changed"},
                                                                              content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response = self.client.put(reverse("driver-detail", args=[3]), data={"last_name": "Changed"},
                                                                              content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_patch(self):
        changed_first_name = "Changed"
        changed_last_name = "Changed-Last"
        response = self.client.patch(reverse("driver-detail", args=[3]), data={"first_name": changed_first_name},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

        response = self.client.patch(reverse("driver-detail", args=[3]), data={"last_name": changed_last_name},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("driver-detail", args=[3]),
                                     content_type="application/json")
        driver = json.loads(response.content)
        self.assertEqual(driver['first_name'], changed_first_name)
        self.assertEqual(driver['last_name'], changed_last_name)

    def test_delete(self):
        response = self.client.delete(reverse("driver-detail", args=[3]),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 204)
        response = self.client.delete(reverse("driver-detail", args=[3]))
        self.assertEqual(response.status_code, 404)