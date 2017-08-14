from django.db.models.signals import post_save
from django.dispatch import receiver


from payments.models import Payment


@receiver(post_save, sender=Payment)
def payment_post_save(sender, instance, **kwargs):
    if not instance._b_paid_status and instance.paid_status:
        #after success pay actions
        pass

