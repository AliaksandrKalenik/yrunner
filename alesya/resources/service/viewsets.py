from rest_framework.generics import RetrieveUpdateDestroyAPIView, \
    ListCreateAPIView
from rest_framework.permissions import AllowAny

from alesya.models import Service
from alesya.resources.service.serializers import ServiceSerializer


class ServiceViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.order_by('id')
    serializer_class = ServiceSerializer
    permission_classes = (AllowAny, )


class ServiceListViewSet(ListCreateAPIView):
    queryset = Service.objects.order_by('id')
    serializer_class = ServiceSerializer
    permission_classes = (AllowAny, )
