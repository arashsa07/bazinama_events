from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.utils import timezone

from utils.send_message import adp_send_sms


User = get_user_model()


class Command(BaseCommand):
    help = 'Send sms to user that register but did not pay.'

    def handle(self, *args, **options):

        msg = render_to_string('unpaid_users.txt')

        one_day_before = timezone.now() - timezone.timedelta(days=1)
        two_days_before = timezone.now() - timezone.timedelta(days=2)

        # WHY??
        users = User.objects.filter(
            date_joined__lt=one_day_before,
            date_joined__gte=two_days_before
        ).exclude(
            phone_number=None
        )

        """
        users = User.objects.filter(
            date_joined__lt=one_day_before,
            date_joined__gte=two_days_before,
            phone_number__isnull=False
        )

        users = User.objects.filter(
            phone_number__isnull=False
        )
        """

        for user in users:
            if user.has_profile and not user.payment_set.filter(paid_status=True):
                sent_message = adp_send_sms(user.phone_number, msg)
                if sent_message:
                    print('Alert sms sent to %s' % user.phone_number)
                else:
                    print('Could not send sms to %s.' % user.phone_number)
