import stripe
import math
from decimal import Decimal

import django.dispatch
from django.dispatch import receiver
from django.conf import settings

from .models import Account, UserStripeSubscription
from Bctpython.signals import webhook_invoice_payment_succeeded


# Define signals
count_points = django.dispatch.Signal(providing_args=['user', 'amount'])
webhook_invoice_payment_succeeded2 = django.dispatch.Signal(providing_args=["full_json"])


# Signal to count user bonus points
@receiver(count_points, sender=None)
def count_user_points(sender, **kwargs):
    user = kwargs['user']
    amount = kwargs['amount']
    # Get points price from settings file
    point_price = settings.POINTS_PER_DOLLAR
    # Define how many points user has
    current_points = user.points
    # Calculate how many points user earned
    new_points = math.floor(float(amount) * point_price)
    # Calculate final amount of points
    final_points = current_points + new_points
    # Update database and set new
    update_user_points = Account.objects.filter(pk=user.pk).update(points=final_points)


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
        # Get Account Username from stripe customer_id
        get_account = Account.objects.prefetch_related('stripe_account_subscription').get(
            stripe_account_subscription__subscription_id=subscription_id)
        # Send signal to update user bonus points
        count_points.send(sender=None, amount=sum_in_dollars, user=get_account)


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
        # Get Account Username from stripe customer_id
        get_account = Account.objects.prefetch_related('stripe_account_subscription').get(
            stripe_account_subscription__subscription_id=subscription_id)
        # Send signal to update user bonus points
        count_points.send(sender=None, amount=sum_in_dollars, user=get_account)


# @receiver(webhook_charge_succeeded, sender=None)
# def add_score2(sender, **kwargs):
#     amount = kwargs['full_json']['data']['object']['amount']
#     debt = amount / 100
#     query = UserStripeSubscription.objects.filter(subscription_id='sub_BQbcotf5gKozwF').update(debt=debt)
