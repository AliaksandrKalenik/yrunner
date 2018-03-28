import rest_framework_filters as filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView, \
    ListCreateAPIView
from rest_framework.permissions import AllowAny

from alesya.models import Entity
from alesya.resources.entity.serializers import EntitySerializer


class EntityViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Entity.objects.order_by('id')
    serializer_class = EntitySerializer
    permission_classes = (AllowAny, )


class EntityFilter(filters.FilterSet):

    class Meta:
        model = Entity
        fields = {
            'id': '__all__',
            'name': '__all__',
            'number': '__all__',
            'project_id': '__all__',
        }


class EntityListViewSet(ListCreateAPIView):
    queryset = Entity.objects.order_by('id')
    serializer_class = EntitySerializer
    permission_classes = (AllowAny, )
    filter_class = EntityFilter
