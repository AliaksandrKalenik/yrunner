from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from alesya.resources.classifier.viewsets import ClassifierViewSet, \
    ClassifierListViewSet
from alesya.resources.entity.viewsets import EntityViewSet, EntityListViewSet
from alesya.resources.tag.viewsets import TagListViewSet, TagViewSet

urlpatterns = [
    url(r'^entity/(?P<pk>[0-9]+)/', EntityViewSet.as_view(), name='entity'),
    url(r'^entity/', EntityListViewSet.as_view(), name='entity-list'),
    url(r'^classifier/(?P<pk>[0-9]+)/', ClassifierViewSet.as_view(), name='classifier'),
    url(r'^classifier/', ClassifierListViewSet.as_view(), name='classifier-list'),
    url(r'^tags/(?P<pk>[0-9]+)/', TagViewSet.as_view(), name='tag'),
    url(r'^tags/', TagListViewSet.as_view(), name='tag-list'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
