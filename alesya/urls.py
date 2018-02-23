from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from alesya.resources.entity.viewsets import EntityViewSet, \
    EntityListViewSet
from alesya.resources.service.viewsets import ServiceViewSet, \
    ServiceListViewSet
from alesya.resources.tag.viewsets import TagListViewSet, TagViewSet

urlpatterns = [
    url(r'^services/(?P<pk>[0-9]+)/', ServiceViewSet.as_view(), name='service'),
    url(r'^services/', ServiceListViewSet.as_view(), name='service-list'),
    url(r'^entities/(?P<pk>[0-9]+)/', EntityViewSet.as_view(), name='entity'),
    url(r'^entities/', EntityListViewSet.as_view(), name='entity-list'),
    url(r'^tags/(?P<pk>[0-9]+)/', TagViewSet.as_view(), name='tag'),
    url(r'^tags/', TagListViewSet.as_view(), name='tag-list'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
