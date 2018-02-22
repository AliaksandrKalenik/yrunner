import json
from django.test import TestCase
from django.urls import reverse

from alesya.models import Classification


class TagTest(TestCase):

    def test_create(self):
        classification = Classification.objects.create(
            name="Location",
        )
        result = self.client.post(
            reverse("tag-list"),
            data={
                'name': "Location",
                'classification': classification.id
            }
        )
        self.assertEqual(result.data['name'], "Location")
        self.assertEqual(result.data['classification'], classification.id)

    def test_update(self):
        classification = Classification.objects.create(
            name="Location",
        )
        result = self.client.post(
            reverse("tag-list"),
            data={
                'name': "Location",
                'classification': classification.id
            }
        )

        result = self.client.patch(
            reverse("tag", kwargs={"pk": result.data['id']}),
            data=json.dumps({
                'name': "Country",
                'classification': None
            }),
            content_type='application/json'
        )
        self.assertEqual(result.data['name'], "Country")
        self.assertIsNone(result.data['classification'])

    def test_list(self):
        classification = Classification.objects.create(
            name="Location",
        )
        self.client.post(
            reverse("tag-list"),
            data={
                'name': "Location",
                'classification': classification.id
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
                    'classification': classification.id
                },
                {
                    'name': "Country",
                    'classification': None
                }
            ]
        )

    def test_read(self):
        classification = Classification.objects.create(
            name="Location",
        )
        result = self.client.post(
            reverse("tag-list"),
            data={
                'name': "Location",
                'classification': classification.id
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
                'classification': classification.id,
            }
        )

    def test_delete(self):
        classification = Classification.objects.create(
            name="Location",
        )
        result = self.client.post(
            reverse("tag-list"),
            data={
                'name': "Location",
                'classification': classification.id
            }
        )
        object_id = result.data['id']
        result = self.client.delete(
            reverse('tag', kwargs={"pk": object_id})
        )
        self.assertEqual(result.status_code, 204)
