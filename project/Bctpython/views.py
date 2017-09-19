import stripe
from django.views.decorators.http import require_http_methods

from django.http import HttpResponse
import json
# try:
#     import json as simplejson
# except:
#     from django.utils import simplejson
from django.views.decorators.http import require_POST
from accounts.models import Account
from django.conf import settings
from .signals import *
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY


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

    json = simplejson.loads(request.POST["json"])

    if json["event"] == "recurring_payment_failed":
        webhook_recurring_payment_failed.send(sender=None,
                                              customer=_try_to_get_customer_from_customer_id(json["customer"]),
                                              full_json=json)

    elif json["event"] == "invoice_ready":
        webhook_invoice_ready.send(sender=None, customer=_try_to_get_customer_from_customer_id(json["customer"]),
                                   full_json=json)

    elif json["event"] == "recurring_payment_succeeded":
        webhook_recurring_payment_succeeded.send(sender=None,
                                                 customer=_try_to_get_customer_from_customer_id(json["customer"]),
                                                 full_json=json)

    elif json["event"] == "subscription_trial_ending":
        webhook_subscription_trial_ending.send(sender=None,
                                               customer=_try_to_get_customer_from_customer_id(json["customer"]),
                                               full_json=json)

    elif json["event"] == "subscription_final_payment_attempt_failed":
        webhook_subscription_final_payment_attempt_failed.send(sender=None,
                                                               customer=_try_to_get_customer_from_customer_id(
                                                                   json["customer"]), full_json=json)

    elif json["event"] == "ping":
        webhook_subscription_ping_sent.send(sender=None)

    else:
        return HttpResponse(status=400)

    return HttpResponse(status=200)


endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


@require_POST
@csrf_exempt
def webhooks_v2(request):
    """
    Handles all known webhooks from stripe, and calls signals.
    Plug in as you need.
    """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    event_json = json.loads(request.body)
    event_key = event_json['type'].replace('.', '_')

    if event_key in WEBHOOK_MAP:
        WEBHOOK_MAP[event_key].send(sender=None, full_json=event_json)

    return HttpResponse(status=200)

#     if request.method != "POST":
#         return HttpResponse("Invalid Request.", status=400)
#
#     try:
#         event_json = json.loads(request.body)
#     except AttributeError:
#         # Backwords compatibility
#         # Prior to Django 1.4, request.body was named request.raw_post_data
#         event_json = json.loads(request.raw_post_data)
#     event_key = event_json['type'].replace('.', '_')
#
#     if event_key in WEBHOOK_MAP:
#         WEBHOOK_MAP[event_key].send(sender=None, full_json=event_json)
#
#     return HttpResponse(status=200)
#
# def my_webhook_view(request):
#   # Retrieve the request's body and parse it as JSON
#   event_json = json.loads(request.body)
#
#   # Do something with event_json
#
#   return HttpResponse(status=200)
