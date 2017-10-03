import math
import stripe
from decimal import Decimal
import django.dispatch
from django.dispatch import receiver
from django.conf import settings
from Bctpython.signals import webhook_invoice_payment_succeeded
from .quickbooks_api import create_invoice, invoice_payment
from .models import Account, UserStripeSubscription

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
    # Get quickbooks customer from subscription
    quickbooks_customer_id = local_subscription.user.quickbooks_account.customer_id
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

        if local_subscription.quickbooks_invoice_id:
            quickbooks_invoice_id = local_subscription.quickbooks_invoice_id
        else:
            create_quickbooks_invoice, status_code = create_invoice(quickbooks_customer_id, float(debt))

            if not status_code >= 400:
                quickbooks_invoice_id = create_quickbooks_invoice['Invoice']['Id']
                set_invoice_id = UserStripeSubscription.objects.filter(subscription_id=subscription_id).update(
                    quickbooks_invoice_id=quickbooks_invoice_id)
            else:
                return

        create_quickbooks_tour_payment, status_code = invoice_payment(quickbooks_customer_id, quickbooks_invoice_id,
                                                                      float(sum_in_dollars))


@receiver(webhook_invoice_payment_succeeded2, sender=None)
def subscription_payment(sender, **kwargs):
    # Define stripe secret key
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # Get data from kwargs
    customer_id = 'cus_BUJF2swMjhQs19'
    # subscription_id = kwargs['full_json']['data']['object']['subscription']
    status = True
    total = 600
    # Get Subscription instance from database
    local_subscription = UserStripeSubscription.objects.filter(user='1').get()
    subscription_id = local_subscription.subscription_id
    # Get quickbooks customer from subscription
    quickbooks_customer_id = local_subscription.user.quickbooks_account.customer_id
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
        test = UserStripeSubscription.objects.filter(user='1').get()
        if test.quickbooks_invoice_id:
            quickbooks_invoice_id = local_subscription.quickbooks_invoice_id
        else:
            create_quickbooks_invoice, status_code = create_invoice(quickbooks_customer_id, float(debt))

            if not status_code >= 400:
                quickbooks_invoice_id = create_quickbooks_invoice['Invoice']['Id']
                set_invoice_id = UserStripeSubscription.objects.filter(subscription_id=subscription_id).update(
                    quickbooks_invoice_id=quickbooks_invoice_id)
            else:
                return
        # if hasattr(test, 'quickbooks_invoice_id'):
        #     quickbooks_invoice_id = local_subscription.quickbooks_invoice_id
        # else:
        #     create_quickbooks_invoice, status_code = create_invoice(quickbooks_customer_id, float(debt))
        #
        #     if not status_code >= 400:
        #         quickbooks_invoice_id = create_quickbooks_invoice['Invoice']['Id']
        #         set_invoice_id = UserStripeSubscription.objects.filter(subscription_id=subscription_id).update(
        #             quickbooks_invoice_id=quickbooks_invoice_id)
        #     else:
        #         return

        create_quickbooks_tour_payment, status_code = invoice_payment(quickbooks_customer_id, quickbooks_invoice_id,
                                                                      float(sum_in_dollars))


# @receiver(webhook_charge_succeeded, sender=None)
# def add_score2(sender, **kwargs):
#     amount = kwargs['full_json']['data']['object']['amount']
#     debt = amount / 100
#     query = UserStripeSubscription.objects.filter(subscription_id='sub_BQbcotf5gKozwF').update(debt=debt)
