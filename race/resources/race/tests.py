import json

from django.test import TestCase
import datetime as dt


class RaceTest(TestCase):

    def test_create_list(self):
        username = 'alex1'
        password = '12345'
        result = self.client.post(
            '/users/register/',
            data={
                'username': username,
                'password': password
            }
        )
        self.assertEqual(result.data['username'], username)
        self.client.post(
            '/race/',
            {
                "distance": 10000,
                "time": dt.time(3, 15).isoformat(),
                "date": dt.date(2018, 1, 1).isoformat(),
            },
            HTTP_AUTHORIZATION="JWT {}".format(result.data['token'])
        )

        result = self.client.get(
            '/race/',
            HTTP_AUTHORIZATION="JWT {}".format(result.data['token'])
        )
        self.assertEqual(result.data.get('count'), 1)

    def test_permissions(self):
        # first user
        username1 = 'alex2'
        password = '12345'
        result = self.client.post(
            '/users/register/',
            data={
                'username': username1,
                'password': password
            }
        )
        token1 = result.data['token']
        self.client.post(
            '/race/',
            {
                "distance": 10000,
                "time": dt.time(3, 15).isoformat(),
                "date": dt.date(2018, 1, 1).isoformat(),
            },
            HTTP_AUTHORIZATION="JWT {}".format(token1)
        )
        result = self.client.get(
            '/race/',
            HTTP_AUTHORIZATION="JWT {}".format(token1)
        )
        self.assertEqual(result.data.get('count'), 1)
        # Second user
        username2 = 'alex3'
        result = self.client.post(
            '/users/register/',
            data={
                'username': username2,
                'password': password
            }
        )
        token2 = result.data['token']
        self.client.post(
            '/race/',
            {
                "distance": 20000,
                "time": dt.time(3, 15).isoformat(),
                "date": dt.date(2018, 1, 1).isoformat(),
            },
            HTTP_AUTHORIZATION="JWT {}".format(token2)
        )
        result = self.client.get(
            '/race/',
            HTTP_AUTHORIZATION="JWT {}".format(token2)
        )
        self.assertEqual(result.data.get('count'), 1)

    def test_read(self):
        username = 'alex4'
        password = '12345'
        result = self.client.post(
            '/users/register/',
            data={
                'username': username,
                'password': password
            }
        )
        token = result.data['token']
        result = self.client.post(
            '/race/',
            {
                "distance": 10000,
                "time": dt.time(3, 15).isoformat(),
                "date": dt.date(2018, 1, 1).isoformat(),
            },
            HTTP_AUTHORIZATION="JWT {}".format(token)
        )

        object_id = result.data["id"]
        result = self.client.get(
            '/race/{}/'.format(object_id),
            HTTP_AUTHORIZATION="JWT {}".format(token)
        )
        self.assertEqual(result.status_code, 200)

    def test_delete(self):
        username = 'alex5'
        password = '12345'
        result = self.client.post(
            '/users/register/',
            data={
                'username': username,
                'password': password
            }
        )
        token = result.data['token']
        result = self.client.post(
            '/race/',
            {
                "distance": 10000,
                "time": dt.time(3, 15).isoformat(),
                "date": dt.date(2018, 1, 1).isoformat(),
            },
            HTTP_AUTHORIZATION="JWT {}".format(token)
        )

        object_id = result.data["id"]
        result = self.client.delete(
            '/race/{}/'.format(object_id),
            HTTP_AUTHORIZATION="JWT {}".format(token)
        )
        self.assertEqual(result.status_code, 204)
        result = self.client.get(
            '/race/{}/'.format(object_id),
            HTTP_AUTHORIZATION="JWT {}".format(token)
        )
        self.assertEqual(result.status_code, 404)

    def test_update(self):
        username = 'alex6'
        password = '12345'
        result = self.client.post(
            '/users/register/',
            data={
                'username': username,
                'password': password
            }
        )
        token = result.data['token']
        result = self.client.post(
            '/race/',
            {
                "distance": 10000,
                "time": dt.time(3, 15).isoformat(),
                "date": dt.date(2018, 1, 1).isoformat(),
            },
            HTTP_AUTHORIZATION="JWT {}".format(token)
        )

        object_id = result.data["id"]
        result = self.client.patch(
            '/race/{}/'.format(object_id),
            json.dumps({
                "distance": 20000,
                "time": dt.time(5, 15).isoformat(),
                "date": dt.date(2017, 1, 1).isoformat(),
            }),
            HTTP_AUTHORIZATION="JWT {}".format(token),
            content_type='application/json'
        )
        self.assertEqual(result.status_code, 200)
        result = self.client.get(
            '/race/{}/'.format(object_id),
            HTTP_AUTHORIZATION="JWT {}".format(token)
        )
        self.assertEqual(result.data['distance'], 20000)
        self.assertEqual(result.data['time'], "05:15:00")
        self.assertEqual(result.data['date'], "2017-01-01")
