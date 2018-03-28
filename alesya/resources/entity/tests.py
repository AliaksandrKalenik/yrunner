import json
from django.test import TestCase
from django.urls import reverse


class EntityTest(TestCase):

    def test_create(self):
        result = self.client.post(
            reverse("entity-list"),
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
            reverse("entity-list"),
            data={
                'number': 1,
                'name': "ByFly Operator",
                'tags': ["internet", "phone"],
            }
        )

        result = self.client.patch(
            reverse("entity", kwargs={"pk": result.data['id']}),
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
            reverse("entity-list"),
            data={
                'number': 1,
                'name': "ByFly Operator",
                'tags': ["internet", "phone"],
                'project_id': 1,
            }
        )
        self.client.post(
            reverse("entity-list"),
            data={
                'number': 2,
                'name': "Velcom",
                'tags': ["internet", "phone", "mobile"],
            }
        )
        result = self.client.get(
            reverse("entity-list")
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
                    'project_id': 1,
                },
                {
                    'number': 2,
                    'name': "Velcom",
                    'tags': ["internet", "phone", "mobile"],
                    'project_id': None,
                }
            ]
        )

    def test_read(self):
        result = self.client.post(
            reverse("entity-list"),
            data={
                'number': 1,
                'name': "ByFly Operator",
                'tags': ["internet", "phone"],
            }
        )
        object_id = result.data['id']
        result = self.client.get(
            reverse('entity', kwargs={"pk": object_id})
        )
        self.assertDictEqual(
            result.data,
            {
                'id': object_id,
                'number': 1,
                'name': "ByFly Operator",
                'tags': ["internet", "phone"],
                'project_id': None,
            }
        )

    def test_delete(self):
        result = self.client.post(
            reverse("entity-list"),
            data={
                'number': 1,
                'name': "ByFly Operator",
                'tags': ["internet", "phone"],
            }
        )
        object_id = result.data['id']
        result = self.client.delete(
            reverse('entity', kwargs={"pk": object_id})
        )
        self.assertEqual(result.status_code, 204)

    def test_duplicate_tags(self):
        result = self.client.post(
            reverse("entity-list"),
            data={
                'number': 1,
                'name': "ByFly Operator",
                'tags': ["internet", "phone", "phone"],
            }
        )
        self.assertSequenceEqual(result.data['tags'], ["internet", "phone"])
