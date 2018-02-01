from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings

from .serializers import RegisterUserSerializer, UserSerializer


USER_MODEL = get_user_model()


class CreateUserView(CreateAPIView):

    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        result = super(CreateUserView, self).create(request, *args, **kwargs)
        user = USER_MODEL.objects.filter(username=request.data['username']).first()
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        result.data['token'] = token
        return result


class UserView(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = USER_MODEL.objects.order_by("id")
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        if not user.is_superuser:
            queryset = queryset.filter(id=user.id)
        return queryset
