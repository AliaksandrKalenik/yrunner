from dynamic_rest.viewsets import DynamicModelViewSet

from image.models import Image
from image.resources.image.serializers import ImageSerializer


class ImageViewSet(DynamicModelViewSet):

    queryset = Image.objects.order_by("id")
    serializer_class = ImageSerializer
    ordering_fields = "__all__"
    ordering = ("id", )
