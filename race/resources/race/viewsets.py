from rest_framework.generics import RetrieveUpdateDestroyAPIView, \
    ListCreateAPIView

from race.models import Race
from race.resources.race.serializers import RaceSerializer


class RaceViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Race.objects.order_by('date')
    serializer_class = RaceSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        if not user.is_superuser:
            queryset = queryset.filter(user=user)
        return queryset


class RaceListViewSet(ListCreateAPIView):
    queryset = Race.objects.order_by('date')
    serializer_class = RaceSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        if not user.is_superuser:
            queryset = queryset.filter(user=user)
        return queryset
