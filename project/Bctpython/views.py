import stripe
import json

from django.http import HttpResponse
from django.conf import settings

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Account
from .signals import *


# Define stripe secret key and endpoint key for webhook security
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


def _try_to_get_customer_from_customer_id(stripe_customer_id):
    try:
        account = Account.objects.get(stripe_account__customer_id=stripe_customer_id)
    except Account.DoesNotExists:
        return None
    else:
        return account


@csrf_exempt
def webhooks(request):
    """
    Handles all known webhooks from stripe, and calls signals.
    Plug in as you need.
    """

    if request.method != "POST":
        return HttpResponse("Invalid Request.", status=400)

    event_json = json.loads(request.POST["json"])

    if event_json["event"] == "recurring_payment_failed":
        webhook_recurring_payment_failed.send(sender=None,
                                              customer=_try_to_get_customer_from_customer_id(event_json["customer"]),
                                              full_json=event_json)

    elif event_json["event"] == "invoice_ready":
        webhook_invoice_ready.send(sender=None, customer=_try_to_get_customer_from_customer_id(event_json["customer"]),
                                   full_json=event_json)

    elif event_json["event"] == "recurring_payment_succeeded":
        webhook_recurring_payment_succeeded.send(sender=None,
                                                 customer=_try_to_get_customer_from_customer_id(event_json["customer"]),
                                                 full_json=event_json)

    elif event_json["event"] == "subscription_trial_ending":
        webhook_subscription_trial_ending.send(sender=None,
                                               customer=_try_to_get_customer_from_customer_id(event_json["customer"]),
                                               full_json=event_json)

    elif event_json["event"] == "subscription_final_payment_attempt_failed":
        webhook_subscription_final_payment_attempt_failed.send(sender=None,
                                                               customer=_try_to_get_customer_from_customer_id(
                                                                   json["customer"]), full_json=event_json)

    elif event_json["event"] == "ping":
        webhook_subscription_ping_sent.send(sender=None)

    else:
        return HttpResponse(status=400)

    return HttpResponse(status=200)


@require_POST
@csrf_exempt
def webhooks_v2(request):
    """
    Handles all known webhooks from stripe, and calls signals.
    Plug in as you need.
    """
    payload = request.body.decode('utf-8')
    # sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', None)
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    event_json = json.loads(payload)
    event_key = event_json['type'].replace('.', '_')

    if event_key in WEBHOOK_MAP:
        WEBHOOK_MAP[event_key].send(sender=None, full_json=event_json)

    return HttpResponse(status=200)
