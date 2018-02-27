import rest_framework_filters as filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView, \
    ListCreateAPIView
from rest_framework.permissions import AllowAny

from alesya.models import Service
from alesya.resources.service.serializers import ServiceSerializer


class ServiceViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.order_by('id')
    serializer_class = ServiceSerializer
    permission_classes = (AllowAny, )


class ServiceFilter(filters.FilterSet):

    class Meta:
        model = Service
        fields = {
            'id': '__all__',
            'name': '__all__',
            'number': '__all__',
            'project_id': '__all__',
        }


class ServiceListViewSet(ListCreateAPIView):
    queryset = Service.objects.order_by('id')
    serializer_class = ServiceSerializer
    permission_classes = (AllowAny, )
    filter_class = ServiceFilter
