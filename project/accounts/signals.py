import django.dispatch
import stripe
from django.conf import settings
from django.dispatch import receiver
from Bctpython.signals import webhook_charge_succeeded, webhook_invoice_payment_succeeded
from .models import Account, UserStripeSubscription
from decimal import Decimal

test_amount = django.dispatch.Signal(providing_args=["amount", "customer"])
webhook_invoice_payment_succeeded2 = django.dispatch.Signal(providing_args=["full_json"])


@receiver(test_amount, sender=None)
def add_score(sender, **kwargs):
    user = kwargs['customer']

    # profile = instance.user_profile
    # profile.score += 1
    # profile.save()
    print('Signal received')
    print(kwargs['customer'])
    print(kwargs['amount'])


@receiver(webhook_charge_succeeded, sender=None)
def add_score2(sender, **kwargs):
    amount = kwargs['full_json']['data']['object']['amount']
    debt = amount / 100
    query = UserStripeSubscription.objects.filter(subscription_id='sub_BQbcotf5gKozwF').update(debt=debt)


@receiver(webhook_invoice_payment_succeeded2, sender=None)
def subscription_payment(sender, **kwargs):
    # Define stripe secret key
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # Get data from kwargs
    customer_id = kwargs['full_json']['data']['object']['customer']
    # subscription_id = kwargs['full_json']['data']['object']['subscription']
    status = kwargs['full_json']['data']['object']['paid']
    total = kwargs['full_json']['data']['object']['total']
    # Get Subscription instance from database
    local_subscription = UserStripeSubscription.objects.filter(user='1').get()
    subscription_id = local_subscription.subscription_id
    # If invoice paid
    if status is True:
        # Strip works with cents, but our database storing dollars, will count sum in dollars:
        sum_in_dollars = total / 100

        # Define current debt for subscription
        debt = local_subscription.debt

        # Count final sum after last payment
        final_sum = debt - Decimal(sum_in_dollars)

        # Count how many payments left
        current_payments = local_subscription.payments
        payments = current_payments - 1

        # If payment was last cancel subscription at stripe
        if payments == 0:
            remote_subscription = stripe.Subscription.retrieve(subscription_id)
            remote_subscription.delete()
        # Update UserStripeSubscription model and set new debt and payments count
        update_local_subscription = UserStripeSubscription.objects.filter(subscription_id=subscription_id).update(
            debt=final_sum, payments=payments)


@receiver(webhook_invoice_payment_succeeded, sender=None)
def invoice_payment_succeeded(sender, **kwargs):
    # Define stripe secret key
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # Get data from kwargs
    customer_id = kwargs['full_json']['data']['object']['customer']
    subscription_id = kwargs['full_json']['data']['object']['subscription']
    status = kwargs['full_json']['data']['object']['paid']
    total = kwargs['full_json']['data']['object']['total']
    # Get Subscription instance from database
    local_subscription = UserStripeSubscription.objects.filter(subscription_id=subscription_id).get()
    # If invoice paid
    if status is True:
        # Strip works with cents, but our database storing dollars, will count sum in dollars:
        sum_in_dollars = total / 100

        # Define current debt for subscription
        debt = local_subscription.debt

        # Count final sum after last payment
        final_sum = debt - Decimal(sum_in_dollars)

        # Count how many payments left
        current_payments = local_subscription.payments
        payments = current_payments - 1

        # If payment was last cancel subscription at stripe
        if payments == 0:
            remote_subscription = stripe.Subscription.retrieve(subscription_id)
            remote_subscription.delete()
        # Update UserStripeSubscription model and set new debt and payments count
        update_local_subscription = UserStripeSubscription.objects.filter(subscription_id=subscription_id).update(
            debt=final_sum, payments=payments)


# @receiver(webhook_invoice_payment_succeeded2, sender=None)
# def subscription_payment(sender, **kwargs):
#     customer_id = kwargs['full_json']['data']['object']['customer']
#     status = kwargs['full_json']['data']['object']['status']
#     qq = UserStripeSubscription.objects.filter(user='1').get()
#     subscription_id = qq.subscription_id
#     amount = 1000 / 100
#     query2 = UserStripeSubscription.objects.filter(subscription_id=subscription_id).get()
#     query3 = query2.debt
#     debt2 = query3 - Decimal(amount)
#     query = UserStripeSubscription.objects.filter(subscription_id=subscription_id).update(debt=debt2)
#     print(subscription_id)
#     print(customer_id)
#     print(status)
#     print(query)