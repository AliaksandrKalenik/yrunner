import json
import tempfile
import math

import operator
import urllib.request
import io
from functools import reduce

from PIL import Image
from rest_framework.test import APITestCase


class ImageTest(APITestCase):

    def test_create(self):
        """
        curl -i -F "origin=@/path/to/file" http://127.0.0.1:8000/image/
        """
        username = 'alex1'
        password = '12345'
        result = self.client.post(
            '/users/register/',
            data={
                'username': username,
                'password': password
            }
        )
        token = result.data['token']
        query_params = [
        ]
        url = "/image/?{query_params}".format(
            query_params="&".join(query_params))

        image = Image.new("RGB", (320, 320), (100, 200, 300))
        tmp_file = tempfile.NamedTemporaryFile(prefix="tmp_image", suffix='.jpg')
        image.save(tmp_file, format="jpeg")
        upload_file = open(tmp_file.name, 'rb')
        data = {
            "origin": upload_file,
        }
        response = json.loads(self.client.post(url, data, format='multipart', HTTP_AUTHORIZATION="JWT {}".format(token)).content.decode())
        origin_url = response["image"]["origin"]

        #  read image result
        download_file = io.BytesIO(urllib.request.urlopen(origin_url).read())
        download_image = Image.open(download_file)

        compare_result = self.is_images_equal(image, download_image)
        #  close files
        upload_file.close()
        tmp_file.close()
        image.close()
        download_image.close()
        #  compare images
        self.assertTrue(compare_result)

        to_delete_fields = ["origin", "id"]
        for field in to_delete_fields:
            del response["image"][field]
        self.assertDictEqual(
            response["image"],
            {
                "optimized": None,
            }
        )
        result = self.client.get('/image/', HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(len(result.data['images']), 1)

    def is_images_equal(self, image1, image2):
        h1 = image1.histogram()
        h2 = image2.histogram()
        rms = math.sqrt(reduce(operator.add, map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
        return bool(rms)
