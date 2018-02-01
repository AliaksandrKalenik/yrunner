from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from image.resources.image.viewsets import ImageViewSet


urlpatterns = [
    url(r'^$', ImageViewSet.as_view({'post': 'create', 'get': 'list'}), name='image'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
