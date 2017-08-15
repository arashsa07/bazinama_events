from django.conf.urls import url
#from django.views.decorators.cache import cache_page

from .views import StateAPIView


urlpatterns = [
    url(r'states/$', StateAPIView.as_view(), name='states-cities'),
]
