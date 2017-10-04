import requests
import json
from django.conf import settings
from Bctpython.celery import app
from accounts.quickbooks_api import create_user, create_invoice, invoice_payment
from .models import QuickBooksDiscoveryDocument, QuickBooksErrorRequest


@app.task
def get_discovery_document():
    r = requests.get(settings.DISCOVERY_DOCUMENT)
    if r.status_code >= 400:
        return 'Error! Connection to discovery document failed!'
    discovery_doc_json = r.json()

    data_dict = {
        'issuer': discovery_doc_json['issuer'],
        'authorization_endpoint': discovery_doc_json['authorization_endpoint'],
        'userinfo_endpoint': discovery_doc_json['userinfo_endpoint'],
        'revocation_endpoint': discovery_doc_json['revocation_endpoint'],
        'token_endpoint': discovery_doc_json['token_endpoint'],
        'jwks_uri': discovery_doc_json['jwks_uri']
    }

    query, created = QuickBooksDiscoveryDocument.objects.update_or_create(data_dict)

    if created is True:
        return 'Your Discovery Document was created!'
    else:
        return 'Your Discovery Document was updated!'


@app.task
def repeat_quickbooks_errors():
    customer_errors = QuickBooksErrorRequest.objects.filter(request_type='Customer', status_code=401,
                                                            successful=False)[:1]

    if customer_errors:
        get_customer_errors = customer_errors.get()
        request = json.loads(get_customer_errors.request_body)
        get_user_username = request['DisplayName']
        get_user_first_name = request['GivenName']
        get_user_last_name = request['FamilyName']
        get_user_email = request['PrimaryEmailAddr']['Address']

        create_quickbooks_customer, status_code = create_user(get_user_username, get_user_first_name,
                                                              get_user_last_name, get_user_email)

        if not status_code >= 400:
            get_customer_errors.successful = True
            get_customer_errors.save()
        else:
            return 'Error %s for customer creation' % status_code

        return 'Customer created'

    invoice_errors = QuickBooksErrorRequest.objects.filter(request_type='Invoice', status_code=401,
                                                           successful=False)[:1]

    if invoice_errors:
        get_invoice_errors = invoice_errors.get()
        request = json.loads(get_invoice_errors.request_body)
        get_customer_id = request['CustomerRef']['value']
        get_general_price = request['Line'][0]['Amount']

        create_quickbooks_invoice, status_code = create_invoice(get_customer_id, get_general_price)

        if not status_code >= 400:
            get_invoice_errors.successful = True
            get_invoice_errors.save()
        else:
            return 'Error %s for invoice creation' % status_code

        return 'Invoice Created'

    payment_errors = QuickBooksErrorRequest.objects.filter(request_type='Payment', status_code=401,
                                                           successful=False)[:1]

    if payment_errors:
        get_payment_errors = payment_errors.get()
        request = json.loads(get_payment_errors.request_body)
        get_customer_id = request['CustomerRef']['value']
        get_invoice_id = request['Line'][0]['LinkedTxn'][0]['TxnId']
        get_invoice_amount = request['TotalAmt']

        create_quickbooks_payment, status_code = invoice_payment(get_customer_id, get_invoice_id, get_invoice_amount)

        if not status_code >= 400:
            get_payment_errors.successful = True
            get_payment_errors.save()
        else:
            return 'Error %s for payment creation' % status_code

        return 'Payment Created'

    return 'There are no QuickBooks errors!'
