"""yrunner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import get_user_model, login
from rest_framework_swagger.views import get_swagger_view

from django.conf import settings

USER_MODEL = get_user_model()


def schema_view(request):
    doc_user, _ = USER_MODEL.objects.get_or_create(
        email='example@paynpark.xyz',
        is_active=True,
    )
    login(request, doc_user)
    view = get_swagger_view(title='Paynpark API')
    response = view(request)
    return response


urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'^users/', include('user.urls')),
    url(r'^race/', include('race.urls')),
    url(r'^image/', include('image.urls')),
    url(r'^documentation/$', schema_view),
] + static('/media/', document_root=settings.MEDIA_ROOT)
