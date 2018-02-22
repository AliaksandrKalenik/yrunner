from rest_framework.generics import RetrieveUpdateDestroyAPIView, \
    ListCreateAPIView
from rest_framework.permissions import AllowAny

from alesya.models import Classification
from alesya.resources.classification.serializers import \
    ClassificationSerializer


class ClassificationViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Classification.objects.order_by('id')
    serializer_class = ClassificationSerializer
    permission_classes = (AllowAny, )


class ClassificationListViewSet(ListCreateAPIView):
    queryset = Classification.objects.order_by('id')
    serializer_class = ClassificationSerializer
    permission_classes = (AllowAny, )
