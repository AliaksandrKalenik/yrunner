from django.middleware.common import CommonMiddleware


class CorsAllMiddleware(CommonMiddleware):

    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        return response
