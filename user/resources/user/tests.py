from django.test import TestCase


class UserTest(TestCase):

    def test_registration(self):
        username = 'alex'
        password = '12345'
        result = self.client.post(
            '/users/register/',
            data={
                'username': username,
                'password': password
            }
        )
        self.assertEqual(result.data['username'], username)
        result = self.client.get(
            '/users/',
            HTTP_AUTHORIZATION="JWT {}".format(result.data['token'])
        )
        self.assertEqual(result.status_code, 200)

    def test_login(self):
        username = 'alex'
        password = '12345'
        result = self.client.post(
            '/users/register/',
            data={
                'username': username,
                'password': password
            }
        )
        self.assertEqual(result.status_code, 201)

        result = self.client.post(
            '/users/api-token-auth/',
            data={
                'username': username,
                'password': password
            }
        )
        result = self.client.get(
            '/users/',
            HTTP_AUTHORIZATION="JWT {}".format(result.data['token'])
        )
        self.assertEqual(result.status_code, 200)
