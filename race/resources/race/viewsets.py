from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

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
    template_name = 'race_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        if not user.is_superuser:
            queryset = queryset.filter(user=user)
        return queryset


class TemplateRaceListViewSet(ListAPIView):
    queryset = Race.objects.order_by('-date')
    serializer_class = RaceSerializer
    template_name = 'race_list.html'
    renderer_classes = (TemplateHTMLRenderer, )
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        return Response({'races': self.queryset.all()})