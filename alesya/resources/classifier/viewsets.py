from rest_framework.generics import RetrieveUpdateDestroyAPIView, \
    ListCreateAPIView
from rest_framework.permissions import AllowAny

from alesya.models import Сlassifier
from alesya.resources.classifier.serializers import \
    ClassifierSerializer


class ClassifierViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Сlassifier.objects.order_by('id')
    serializer_class = ClassifierSerializer
    permission_classes = (AllowAny, )


class ClassifierListViewSet(ListCreateAPIView):
    queryset = Сlassifier.objects.order_by('id')
    serializer_class = ClassifierSerializer
    permission_classes = (AllowAny, )
