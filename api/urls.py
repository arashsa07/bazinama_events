from django.conf.urls import url
from django.views.decorators.cache import cache_page

from .views import StateAPIView


urlpatterns = [
    url(r'states/$', cache_page(60*60*6)(StateAPIView.as_view())),
]

