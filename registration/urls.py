from django.conf.urls import url

from .views import ProfileAPIView, RegisterAPIView
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token


urlpatterns = [
    url(r'^register/', RegisterAPIView.as_view()),
    url(r'^obtain-token/', obtain_jwt_token),
    url(r'^refresh-token/', refresh_jwt_token),

    url(r'^profile/$', ProfileAPIView.as_view(), name='profile-detail'),
]
