from rest_framework.generics import RetrieveUpdateDestroyAPIView, \
    ListCreateAPIView
from rest_framework.permissions import AllowAny

from alesya.models import Entity
from alesya.resources.entity.serializers import \
    EntitySerializer


class EntityViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Entity.objects.order_by('id')
    serializer_class = EntitySerializer
    permission_classes = (AllowAny, )


class EntityListViewSet(ListCreateAPIView):
    queryset = Entity.objects.order_by('id')
    serializer_class = EntitySerializer
    permission_classes = (AllowAny, )
