import json
from django.test import TestCase
from django.urls import reverse
from alesya.models import Entity


class TagTest(TestCase):

    def test_create(self):
        entity = Entity.objects.create(
            name="Location",
        )
        result = self.client.post(
            reverse("tag-list"),
            data={
                'name': "Location",
                'entity': entity.id
            }
        )
        self.assertEqual(result.data['name'], "Location")
        self.assertEqual(result.data['entity'], entity.id)

    def test_update(self):
        entity = Entity.objects.create(
            name="Location",
        )
        result = self.client.post(
            reverse("tag-list"),
            data={
                'name': "Location",
                'entity': entity.id
            }
        )

        result = self.client.patch(
            reverse("tag", kwargs={"pk": result.data['id']}),
            data=json.dumps({
                'name': "Country",
                'entity': None
            }),
            content_type='application/json'
        )
        self.assertEqual(result.data['name'], "Country")
        self.assertIsNone(result.data['entity'])

    def test_list(self):
        entity = Entity.objects.create(
            name="Location",
        )
        self.client.post(
            reverse("tag-list"),
            data={
                'name': "Location",
                'entity': entity.id
            }
        )
        self.client.post(
            reverse("tag-list"),
            data={
                'name': "Country",
            }
        )
        result = self.client.get(
            reverse("tag-list")
        )
        self.assertEqual(result.data['count'], 2)
        for item in result.data['results']:
            item.pop("id")
        self.assertSequenceEqual(
            result.data['results'],
            [
                {
                    'name': "Location",
                    'entity': entity.id
                },
                {
                    'name': "Country",
                    'entity': None
                }
            ]
        )

    def test_read(self):
        entity = Entity.objects.create(
            name="Location",
        )
        result = self.client.post(
            reverse("tag-list"),
            data={
                'name': "Location",
                'entity': entity.id
            }
        )
        object_id = result.data['id']
        result = self.client.get(
            reverse('tag', kwargs={"pk": object_id})
        )
        self.assertDictEqual(
            result.data,
            {
                'id': object_id,
                'name': "Location",
                'entity': entity.id,
            }
        )

    def test_delete(self):
        entity = Entity.objects.create(
            name="Location",
        )
        result = self.client.post(
            reverse("tag-list"),
            data={
                'name': "Location",
                'entity': entity.id
            }
        )
        object_id = result.data['id']
        result = self.client.delete(
            reverse('tag', kwargs={"pk": object_id})
        )
        self.assertEqual(result.status_code, 204)

    def test_bulk_create(self):
        entity = Entity.objects.create(
            name="Location",
        )
        result = self.client.post(
            reverse("tag-list"),
            data=json.dumps([
                {
                    'name': "Location",
                    'entity': entity.id
                },
                {
                    'name': "Country"
                },
                {
                    'name': "City",
                    'entity': None,
                }
            ]),
            content_type='application/json'
        )
        for item in result.data:
            item.pop("id")
        self.assertSequenceEqual(
            result.data,
            [
                {
                    'name': "Location",
                    'entity': entity.id
                },
                {
                    'name': "Country",
                    'entity': None,
                },
                {
                    'name': "City",
                    'entity': None,
                }
            ]
        )

    def test_bulk_update(self):
        entity = Entity.objects.create(
            name="Location",
        )
        result = self.client.post(
            reverse("tag-list"),
            data=json.dumps([
                {
                    'name': "Location",
                    'entity': entity.id
                },
                {
                    'name': "Country"
                },
                {
                    'name': "City",
                    'entity': None,
                }
            ]),
            content_type='application/json'
        )
        update_data = []
        for item in result.data:
            item["name"] += " updated"
            if item["entity"]:
                item["entity"] = None
            else:
                item["entity"] = entity.id
            update_data.append(item)

        result = self.client.patch(
            reverse("tag-list"),
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertSequenceEqual(
            result.data,
            update_data,
        )

    def test_bulk_delete(self):
        entity = Entity.objects.create(
            name="Location",
        )
        result = self.client.post(
            reverse("tag-list"),
            data=json.dumps([
                {
                    'name': "Location",
                    'entity': entity.id
                },
                {
                    'name': "Country"
                },
                {
                    'name': "City",
                    'entity': None,
                }
            ]),
            content_type='application/json'
        )
        delete_ids = []
        for item in result.data:
            delete_ids.append(str(item["id"]))
        url = reverse("tag-list") + "?id__in={}".format(",".join(delete_ids))

        result = self.client.delete(
            url,
        )
        self.assertEqual(result.status_code, 204)
        result = self.client.get(
            reverse("tag-list"),
        )
        self.assertEqual(result.data.get("count"), 0)
