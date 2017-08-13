from django.conf.urls import include, url
from django.views.decorators.cache import cache_page

from rest_framework.routers import DefaultRouter

from .views import StateViewSet


router = DefaultRouter()
router.register(r'states', StateViewSet)



urlpatterns = [
    url(r'^', include(router.urls)),
]

print(router.urls)
print(urlpatterns)
