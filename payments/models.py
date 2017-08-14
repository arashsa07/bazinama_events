import json
import uuid

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _

from payments.gateways.vas import do_settle
from .gateways import verify_shaparak, verify_saman, verify_raad, verify_bazaar


class Gateway(models.Model):
    TYPE_BANK = 1
    TYPE_PSP = 2
    GATEWAY_TYPES = (
        (TYPE_BANK, _('BANK')),
        (TYPE_PSP, _('PSP')),
    )

    FUNCTION_SAMAN = 1
    FUNCTION_SHAPARAK = 2
    FUNCTION_RAAD = 3
    FUNCTION_BAZAAR = 4
    FUNCTION_VAS = 5
    GATEWAY_FUNCTIONS = (
        (FUNCTION_SAMAN, _('Saman')),
        (FUNCTION_SHAPARAK, _('Shaparak')),
        (FUNCTION_RAAD, _('Raad')),
        (FUNCTION_BAZAAR, _('Bazaar')),
        (FUNCTION_VAS, _('vas')),
    )

    created_time = models.DateTimeField(verbose_name=_('Creation On'), auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=_('Modified On'), auto_now=True)
    title = models.CharField(max_length=100, verbose_name=_("gateway title"))
    merchant_id = models.CharField(max_length=50, verbose_name=_("merchant id"), null=True, blank=True)
    merchant_pass = models.CharField(max_length=50, verbose_name=_("merchant pass"), null=True, blank=True)
    url = models.CharField(max_length=150, verbose_name=_("request url"), null=True, blank=True)
    check_url = models.CharField(max_length=150, verbose_name=_("pay check url"), null=True, blank=True)
    gw_code = models.PositiveSmallIntegerField(verbose_name=_("gateway code"), choices=GATEWAY_FUNCTIONS)
    gw_type = models.PositiveSmallIntegerField(verbose_name=_("gateway type"), choices=GATEWAY_TYPES)
    is_enable = models.BooleanField(_('is enable'), default=True)

    class Meta:
        db_table = 'payments_gateways'
        verbose_name = _("gateway")
        verbose_name_plural = _("gateways")

    def __str__(self):
        return self.title


class Payment(models.Model):
    RESPONSE_APP = 1
    RESPONSE_WEB = 2
    response_type_choices = (
        (RESPONSE_APP, _("mobile")),
        (RESPONSE_WEB, _("web"))
    )
    created_time = models.DateTimeField(verbose_name=_('Creation On'), auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(verbose_name=_('Modified On'), auto_now=True)
    invoice_number = models.UUIDField(verbose_name=_("invoice number"), unique=True, default=uuid.uuid4)
    amount = models.PositiveIntegerField(verbose_name=_("payment amount"), editable=False)
    reference_id = models.CharField(max_length=100, verbose_name=_("reference id"), db_index=True, blank=True)
    user_reference = models.CharField(max_length=100, verbose_name=_("customer reference"), blank=True)
    result_code = models.CharField(max_length=100, verbose_name=_("result code"), blank=True)
    gateway = models.ForeignKey(Gateway, related_name="payments", null=True, blank=True,
                                verbose_name=_("payment gateway"))
    paid_status = models.NullBooleanField(verbose_name=_("is paid status"), default=False, editable=False)
    log = models.TextField(verbose_name=_("payment log"), blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), null=True)
    vas_token = models.CharField(_("vas token for vas payments"), max_length=100, null=True, blank=True)
    response_type = models.PositiveIntegerField(verbose_name=_("response type"), default=RESPONSE_APP,
                                                choices=response_type_choices)

    class Meta:
        db_table = 'payments'
        verbose_name = _("payment")
        verbose_name_plural = _("payments")

    def __str__(self):
        return self.invoice_number.__str__()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._b_paid_status = self.paid_status

    def get_url(self, request=None, gateway=None):
        if request and gateway:
            return "%s?invoice_number=%s&gateway=%s" % (
                request.build_absolute_uri(reverse('payment-gateway')),
                self.invoice_number,
                gateway['id'])
        else:
            return "%s/gateway/?invoice_number=%s&gateway=" % (settings.BASE_URL, self.invoice_number)

    def verify(self, received_data):
        """
        method to do payment related to choosen gateway
        this method use gateway code to detect the gateway
        :param received_data: post data parameters that send from bank after a payment
        :return: true or false in diffrent situation of payment
        """

        # received date log as a json dump in both fail or success
        try:
            self.log = json.dumps(received_data)
        except:
            pass

        if self.gateway.gw_type == self.gateway.TYPE_BANK:

            # on fake response
            if settings.DEVEL:
                self.paid_status = True
                self.reference_id = '111111111'
                self.user_reference = '11111111'

                self.save()
                return True

            self.result_code = received_data["State"]

            # first check status ... if fail only log and return false
            if self.result_code != "OK":
                self.save(update_fields=['updated_time', 'log', 'result_code'])
                return False

            # in a ok payment state
            self.reference_id = received_data["RefNum"]

            if "TRACENO" in received_data:
                self.user_reference = received_data["TRACENO"]

            # verify payment based on the gw_code
            if self.gateway.gw_code == self.gateway.FUNCTION_SAMAN:
                self.paid_status = verify_saman(self.gateway.check_url, self.reference_id, self.gateway.merchant_id,
                                                self.amount * 10)

            if self.gateway.gw_code == self.gateway.FUNCTION_SHAPARAK:
                self.paid_status = verify_shaparak(self.gateway, self.reference_id, self.amount * 10)

            self.save()

        if self.gateway.gw_type == self.gateway.TYPE_PSP:

            if self.gateway.gw_code == self.gateway.FUNCTION_RAAD:
                self.paid_status = verify_raad(received_data.get("payAuth", ''), received_data.get("userToken", ''),
                                               self.amount)

            if self.gateway.gw_code == self.gateway.FUNCTION_BAZAAR:
                if self.check_purchase_token(
                        received_data.get("purchase_token")
                ):
                    self.save()
                    return True
                result = verify_bazaar(
                    received_data.get("package_name", ''),
                    received_data.get("product_id", ''),
                    received_data.get("purchase_token", ''),
                    received_data.get("item_type", ''),
                )
                if result:
                    self.reference_id = received_data.get(
                        "purchase_token")
                self.paid_status = result

            if self.gateway.gw_code == self.gateway.FUNCTION_VAS:
                try:
                    self.paid_status = do_settle(
                        self.vas_token, self.amount)

                except Exception as e:
                    self.paid_status = False

            self.save()
        return self.paid_status

    @classmethod
    def check_purchase_token(cls, token):
        return cls.objects.filter(reference_id=token).exists()

    @classmethod
    def find_purchase(cls, user, received_data):
        payment = cls.objects.select_related('gateway').filter(user=user,
                                                               paid_status=False,
                                                               amount=received_data.get("product_id"),
                                                               gateway=Gateway.FUNCTION_BAZAAR
                                                               ).last()
        if not payment:
            return cls.check_purchase_token(received_data.get("purchase_token"))
        return payment.verify(received_data)
