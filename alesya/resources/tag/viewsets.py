import rest_framework_filters as filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView

from alesya.models import Tag
from alesya.resources.tag.serializers import TagSerializer


class TagViewSet(RetrieveUpdateDestroyAPIView):

    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )


class TagFilter(filters.FilterSet):

    class Meta:
        model = Tag
        fields = {
            'name': '__all__',
            'id': '__all__'
        }


class TagListViewSet(ListBulkCreateUpdateDestroyAPIView):

    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    filter_class = TagFilter
