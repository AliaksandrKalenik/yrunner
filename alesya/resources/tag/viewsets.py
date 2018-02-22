from rest_framework.generics import RetrieveUpdateDestroyAPIView, \
    ListCreateAPIView
from rest_framework.permissions import AllowAny

from alesya.models import Tag
from alesya.resources.tag.serializers import TagSerializer


class TagViewSet(RetrieveUpdateDestroyAPIView):

    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )


class TagListViewSet(ListCreateAPIView):

    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
