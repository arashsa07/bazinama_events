from django.conf.urls import url

from .views import PaymentPayView, PaymentResultView

urlpatterns = [
    url(r'^pay/$', PaymentPayView.as_view(), name='payment-pay'),
    url(r'^result/$', PaymentResultView.as_view(), name='payment-result'),
]
