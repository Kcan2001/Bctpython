import requests
import json
from django.utils import timezone
from django.conf import settings
from quickbooks.models import QuickBooksToken, QuickBooksErrorRequest
from quickbooks.utils import get_bearer_token_from_refresh_token


def create_user(username, first_name, last_name, email):
    query = QuickBooksToken.objects.first()
    access_token = query.quickbooks_access_token
    realm_id = query.quickbooks_realm_id
    refresh_token = query.quickbooks_refresh_token

    route = '/v3/company/{0}/customer'.format(realm_id)
    auth_header = 'Bearer ' + access_token
    headers = {'Authorization': auth_header, 'Accept': 'application/json', 'Content-type': 'application/json'}
    payload = {
        'DisplayName': username,
        'GivenName': first_name,
        'FamilyName': last_name,
        'PrimaryEmailAddr': {
            'Address': email
        },
        'Taxable': False
    }
    r = requests.post(settings.SANDBOX_QBO_BASEURL + route, data=json.dumps(payload), headers=headers)
    status_code = r.status_code

    # todo check all statuses
    if status_code >= 400:
        # if call to QBO doesn't succeed then get a new bearer token from refresh token and try again
        bearer = get_bearer_token_from_refresh_token(refresh_token)
        query = QuickBooksToken.objects.update(
            quickbooks_access_token=bearer.access_token,
            quickbooks_access_token_expires_in=bearer.access_token_expire,
            quickbooks_access_token_updated=timezone.now(),
            quickbooks_refresh_token=bearer.refresh_token,
            quickbooks_refresh_token_expires_in=bearer.refresh_token_expire,
            quickbooks_refresh_token_updated=timezone.now()
        )

        auth_header = 'Bearer ' + bearer.access_token
        headers = {'Authorization': auth_header, 'Accept': 'application/json', 'Content-type': 'application/json'}

        r = requests.post(settings.SANDBOX_QBO_BASEURL + route, data=json.dumps(payload), headers=headers)
        status_code = r.status_code

        if status_code >= 400:
            query = QuickBooksErrorRequest.objects.create(request_type='Customer', request_body=r.request.body,
                                                          request_headers=r.request.headers, request_url=r.request.url,
                                                          status_code=r.status_code, response_text=r.text,
                                                          successful=False)
            return status_code

    response = json.loads(r.text)
    return response, status_code


def create_and_pay_invoice(customer_id, general_price):
    invoice, status_code = create_invoice(customer_id, general_price)

    if not status_code >= 400:
        invoice_id = invoice['Invoice']['Id']
        invoice_amount = invoice['Invoice']['TotalAmt']

        payment, status_code = invoice_payment(customer_id, invoice_id, invoice_amount)

    return status_code


def create_invoice(customer_id, general_price):
    query = QuickBooksToken.objects.first()
    access_token = query.quickbooks_access_token
    refresh_token = query.quickbooks_refresh_token
    realm_id = query.quickbooks_realm_id
    route = '/v3/company/{0}/invoice'.format(realm_id)
    auth_header = 'Bearer ' + access_token
    headers = {'Authorization': auth_header, 'Accept': 'application/json', 'Content-type': 'application/json'}
    payload = {
        'Line': [
            {
                'Amount': general_price,
                'DetailType': 'SalesItemLineDetail',
                'SalesItemLineDetail': {
                    'ItemRef': {
                        'value': '1'
                    }
                }
            }
        ],
        'CustomerRef': {
            'value': customer_id
        }
    }
    r = requests.post(settings.SANDBOX_QBO_BASEURL + route, data=json.dumps(payload), headers=headers)
    status_code = r.status_code

    # todo check all statuses
    if status_code >= 400:
        # if call to QBO doesn't succeed then get a new bearer token from refresh token and try again
        bearer = get_bearer_token_from_refresh_token(refresh_token)
        query = QuickBooksToken.objects.update(
            quickbooks_access_token=bearer.access_token,
            quickbooks_access_token_expires_in=bearer.access_token_expire,
            quickbooks_access_token_updated=timezone.now(),
            quickbooks_refresh_token=bearer.refresh_token,
            quickbooks_refresh_token_expires_in=bearer.refresh_token_expire,
            quickbooks_refresh_token_updated=timezone.now()
        )

        auth_header = 'Bearer ' + bearer.access_token
        headers = {'Authorization': auth_header, 'Accept': 'application/json', 'Content-type': 'application/json'}

        r = requests.post(settings.SANDBOX_QBO_BASEURL + route, data=json.dumps(payload), headers=headers)
        status_code = r.status_code

        if status_code >= 400:
            query = QuickBooksErrorRequest.objects.create(request_type='Invoice', request_body=r.request.body,
                                                          request_headers=r.request.headers, request_url=r.request.url,
                                                          status_code=r.status_code, response_text=r.text,
                                                          successful=False)
            return status_code

    response = json.loads(r.text)
    return response, status_code


def invoice_payment(customer_id, invoice_id, invoice_amount):
    query = QuickBooksToken.objects.first()
    access_token = query.quickbooks_access_token
    refresh_token = query.quickbooks_refresh_token
    realm_id = query.quickbooks_realm_id
    route = '/v3/company/{0}/payment'.format(realm_id)
    auth_header = 'Bearer ' + access_token
    headers = {'Authorization': auth_header, 'Accept': 'application/json', 'Content-type': 'application/json'}
    payload = {
        'CustomerRef': {
            'value': customer_id
        },
        'TotalAmt': invoice_amount,
        'Line': [
            {
                'Amount': invoice_amount,
                'LinkedTxn': [
                    {
                        'TxnId': invoice_id,
                        'TxnType': 'Invoice'
                    }
                ]
            }
        ]
    }
    r = requests.post(settings.SANDBOX_QBO_BASEURL + route, data=json.dumps(payload), headers=headers)
    status_code = r.status_code

    # todo check all statuses
    if status_code >= 400:
        # if call to QBO doesn't succeed then get a new bearer token from refresh token and try again
        bearer = get_bearer_token_from_refresh_token(refresh_token)
        query = QuickBooksToken.objects.update(
            quickbooks_access_token=bearer.access_token,
            quickbooks_access_token_expires_in=bearer.access_token_expire,
            quickbooks_access_token_updated=timezone.now(),
            quickbooks_refresh_token=bearer.refresh_token,
            quickbooks_refresh_token_expires_in=bearer.refresh_token_expire,
            quickbooks_refresh_token_updated=timezone.now()
        )

        auth_header = 'Bearer ' + bearer.access_token
        headers = {'Authorization': auth_header, 'Accept': 'application/json', 'Content-type': 'application/json'}

        r = requests.post(settings.SANDBOX_QBO_BASEURL + route, data=json.dumps(payload), headers=headers)
        status_code = r.status_code

        if status_code >= 400:
            query = QuickBooksErrorRequest.objects.create(request_type='Payment', request_body=r.request.body,
                                                          request_headers=r.request.headers, request_url=r.request.url,
                                                          status_code=r.status_code, response_text=r.text,
                                                          successful=False)
            return status_code

    response = json.loads(r.text)
    return response, status_code
