from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from user.resources.user.viewsets import CreateUserView, UserView

urlpatterns = [
    # auth
    url(r'^register', CreateUserView.as_view(), name='register-user'),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),

    # user
    url(r'^$', UserView.as_view(), name='users'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
