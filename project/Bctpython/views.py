import stripe
import json
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .signals import *


# Define stripe secret key and endpoint key for webhook security
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


@require_POST
@csrf_exempt
def webhooks(request):
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
