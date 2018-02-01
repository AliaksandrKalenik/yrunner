import json

from django.test import TestCase
import datetime as dt


class RaceReportTest(TestCase):

    def test_report(self):
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
            '/race/week_report/',
            {
                "start_date": dt.date(2017, 12, 1),
                "end_date": dt.date(2018, 2, 1),
            },
            HTTP_AUTHORIZATION="JWT {}".format(result.data['token'])
        )
        self.assertEqual(len(result.data), 7)
