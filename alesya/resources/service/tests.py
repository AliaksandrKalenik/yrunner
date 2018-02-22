import json
from django.test import TestCase
from django.urls import reverse


class ServiceTest(TestCase):

    def test_create(self):
        result = self.client.post(
            reverse("service-list"),
            data={
                'number': 1,
                'name': "ByFly Operator",
                'tags': ["internet", "phone"],
            }
        )
        self.assertEqual(result.data['number'], 1)
        self.assertEqual(result.data['name'], "ByFly Operator")
        self.assertSequenceEqual(result.data['tags'], ["internet", "phone"])

    def test_update(self):
        result = self.client.post(
            reverse("service-list"),
            data={
                'number': 1,
                'name': "ByFly Operator",
                'tags': ["internet", "phone"],
            }
        )

        result = self.client.patch(
            reverse("service", kwargs={"pk": result.data['id']}),
            data=json.dumps({
                'number': 2,
                'name': "ByFly Operator2",
                'tags': ["phone", "internet"],
            }),
            content_type='application/json'
        )
        self.assertEqual(result.data['number'], 2)
        self.assertEqual(result.data['name'], "ByFly Operator2")
        self.assertSequenceEqual(result.data['tags'], ["phone", "internet"])

    def test_list(self):
        self.client.post(
            reverse("service-list"),
            data={
                'number': 1,
                'name': "ByFly Operator",
                'tags': ["internet", "phone"],
            }
        )
        self.client.post(
            reverse("service-list"),
            data={
                'number': 2,
                'name': "Velcom",
                'tags': ["internet", "phone", "mobile"],
            }
        )
        result = self.client.get(
            reverse("service-list")
        )
        self.assertEqual(result.data['count'], 2)
        for item in result.data['results']:
            item.pop("id")
        self.assertSequenceEqual(
            result.data['results'],
            [
                {
                    'number': 1,
                    'name': "ByFly Operator",
                    'tags': ["internet", "phone"],
                },
                {
                    'number': 2,
                    'name': "Velcom",
                    'tags': ["internet", "phone", "mobile"],
                }
            ]
        )

    def test_read(self):
        result = self.client.post(
            reverse("service-list"),
            data={
                'number': 1,
                'name': "ByFly Operator",
                'tags': ["internet", "phone"],
            }
        )
        object_id = result.data['id']
        result = self.client.get(
            reverse('service', kwargs={"pk": object_id})
        )
        self.assertDictEqual(
            result.data,
            {
                'id': object_id,
                'number': 1,
                'name': "ByFly Operator",
                'tags': ["internet", "phone"],
            }
        )

    def test_delete(self):
        result = self.client.post(
            reverse("service-list"),
            data={
                'number': 1,
                'name': "ByFly Operator",
                'tags': ["internet", "phone"],
            }
        )
        object_id = result.data['id']
        result = self.client.delete(
            reverse('service', kwargs={"pk": object_id})
        )
        self.assertEqual(result.status_code, 204)

    def test_duplicate_tags(self):
        result = self.client.post(
            reverse("service-list"),
            data={
                'number': 1,
                'name': "ByFly Operator",
                'tags': ["internet", "phone", "phone"],
            }
        )
        self.assertSequenceEqual(result.data['tags'], ["internet", "phone"])
