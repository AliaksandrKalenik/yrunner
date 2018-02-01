from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from race.resources.race.viewsets import RaceViewSet, RaceListViewSet

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)', RaceViewSet.as_view(), name='race'),
    url(r'^$', RaceListViewSet.as_view(), name='race-list'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
