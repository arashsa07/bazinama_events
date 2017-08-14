from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PaymentAppConfig(AppConfig):
    name = 'payments'
    verbose_name = _('payments')

    def ready(self):
        import payments.signals