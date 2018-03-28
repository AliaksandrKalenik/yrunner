import rest_framework_filters as filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView

from alesya.models import ClassifierTag
from alesya.resources.tag.serializers import ClassifierTagSerializer


class TagViewSet(RetrieveUpdateDestroyAPIView):

    queryset = ClassifierTag.objects.order_by("id")
    serializer_class = ClassifierTagSerializer
    permission_classes = (AllowAny, )


class TagFilter(filters.FilterSet):

    class Meta:
        model = ClassifierTag
        fields = {
            'name': '__all__',
            'id': '__all__'
        }


class TagListViewSet(ListBulkCreateUpdateDestroyAPIView):

    queryset = ClassifierTag.objects.order_by("id")
    serializer_class = ClassifierTagSerializer
    permission_classes = (AllowAny, )
    filter_class = TagFilter
