import django.dispatch
from django.dispatch import receiver
from Bctpython.signals import webhook_invoice_payment_failed
from .models import Account, UserStripeSubscription
from decimal import Decimal

test_amount = django.dispatch.Signal(providing_args=["amount", "customer"])
webhook_invoice_payment_succeeded = django.dispatch.Signal(providing_args=["full_json"])


@receiver(test_amount, sender=None)
def add_score(sender, **kwargs):
    user = kwargs['customer']

    # profile = instance.user_profile
    # profile.score += 1
    # profile.save()
    print('Signal received')
    print(kwargs['customer'])
    print(kwargs['amount'])


@receiver(webhook_invoice_payment_succeeded, sender=None)
def subscription_payment(sender, **kwargs):
    customer_id = kwargs['full_json']['data']['object']['customer']
    status = kwargs['full_json']['data']['object']['status']
    qq = UserStripeSubscription.objects.filter(user='1').get()
    subscription_id = qq.subscription_id
    amount = 1000 / 100
    query2 = UserStripeSubscription.objects.filter(subscription_id=subscription_id).get()
    query3 = query2.debt
    debt2 = query3 - Decimal(amount)
    query = UserStripeSubscription.objects.filter(subscription_id=subscription_id).update(debt=debt2)
    print(subscription_id)
    print(customer_id)
    print(status)
    print(query)

# test_amount.connect(add_score, sender=None)
