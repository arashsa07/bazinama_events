from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Payment, Gateway
# from registration.models import User, UserProfile


PAYMENT_PROJECT_NAME = 'royaljaam'
PAYMENT_AMOUNT = 2000  # 2000 toman


def render_bank_page(request, invoice_id, request_url, merchant_id, amount, **kwargs):
    """
    send parameters to a template ... template contain a form include thease parameters
    this form automatically submit to bank url
    """
    render_context = {
        "invoice_id": invoice_id,
        "request_url": request_url,
        "merchant_id": merchant_id,
        "redirect_url": request.build_absolute_uri(reverse('payment-result')),
        "amount": amount * 10,
        "extra_data": kwargs,
    }
    return render(request, 'payments/pay.html', context=render_context)


class PaymentPayView(APIView):
    """
     Redirect to bank payment page.
    """
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentPayView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        gateway = Gateway.objects.first()
        user = request.user

        if user.has_profile:
            payment = Payment.objects.create(
                amount=PAYMENT_AMOUNT,
                gateway=gateway,
                response_type=Payment.RESPONSE_WEB,
                user=user
            )

            return render_bank_page(
                    request,
                    payment.invoice_number,
                    gateway.url,
                    gateway.merchant_id,
                    payment.amount,
                    ResNum1=PAYMENT_PROJECT_NAME
                )

        return Response({'detail': _('Profile is not set for this user.')}, status=status.HTTP_401_UNAUTHORIZED)


class PaymentResultView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentResultView, self).dispatch(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request):
        """
        Show bank response
        """
        payment_status = False
        received_data = request.POST
        invoice_number = received_data.get("ResNum")

        if not invoice_number:
            return Response({'detail': _('No response from bank')}, status=status.HTTP_204_NO_CONTENT)

        try:
            payment = Payment.objects.select_related('gateway').select_for_update().get(invoice_number=invoice_number)
        except Payment.DoesNotExist:
            pass
        except Exception as e:
            pass
        else:
            # if payment was not paid before ...
            if not payment.paid_status:
                payment_status = payment.verify(received_data)
            else:
                payment_status = payment.paid_status

        response = {
            'payment_status': payment_status,
            'invoice_number': invoice_number
        }

        return JsonResponse(response)
