import json
from django.test import TestCase
from django.urls import reverse


class EntityTest(TestCase):

    def test_create(self):
        result = self.client.post(
            reverse("entity-list"),
            data={
                'name': "Location",
                'belong_to_class_question': "Has it have location?",
                'question': "Where?",
            }
        )
        self.assertEqual(result.data['name'], "Location")
        self.assertEqual(result.data['belong_to_class_question'], "Has it have location?")
        self.assertSequenceEqual(result.data['question'], "Where?")

    def test_update(self):
        result = self.client.post(
            reverse("entity-list"),
            data={
                'name': "Location",
                'belong_to_class_question': "Has it have location?",
                'question': "Where?",
            }
        )

        result = self.client.patch(
            reverse("entity", kwargs={"pk": result.data['id']}),
            data=json.dumps({
                'name': "Country",
                'belong_to_class_question': "Has it have county beloning?",
                'question': "In what country?",
            }),
            content_type='application/json'
        )
        self.assertEqual(result.data['name'], "Country")
        self.assertEqual(result.data['belong_to_class_question'], "Has it have county beloning?")
        self.assertSequenceEqual(result.data['question'], "In what country?")

    def test_list(self):
        self.client.post(
            reverse("entity-list"),
            data={
                'name': "Location",
                'belong_to_class_question': "Has it have location?",
                'question': "Where?",
            }
        )
        self.client.post(
            reverse("entity-list"),
            data={
                'name': "Country",
                'belong_to_class_question': "Has it have county beloning?",
                'question': "In what country?",
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
                    'name': "Location",
                    'belong_to_class_question': "Has it have location?",
                    'question': "Where?",
                },
                {
                    'name': "Country",
                    'belong_to_class_question': "Has it have county beloning?",
                    'question': "In what country?",
                }
            ]
        )

    def test_read(self):
        result = self.client.post(
            reverse("entity-list"),
            data={
                'name': "Location",
                'belong_to_class_question': "Has it have location?",
                'question': "Where?",
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
                'name': "Location",
                'belong_to_class_question': "Has it have location?",
                'question': "Where?",
            }
        )

    def test_delete(self):
        result = self.client.post(
            reverse("entity-list"),
            data={
                'name': "Location",
                'belong_to_class_question': "Has it have location?",
                'question': "Where?",
            }
        )
        object_id = result.data['id']
        result = self.client.delete(
            reverse('entity', kwargs={"pk": object_id})
        )
        self.assertEqual(result.status_code, 204)
