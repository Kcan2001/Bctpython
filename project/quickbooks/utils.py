import requests
import json
import base64
import random
from django.conf import settings
from .models import Bearer, QuickBooksDiscoveryDocument


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

    return created


def get_bearer_token(auth_code):
    discovery_document = QuickBooksDiscoveryDocument.objects.first()
    token_endpoint = discovery_document.token_endpoint
    auth_header = 'Basic ' + string_to_base64(settings.CLIENT_ID + ':' + settings.CLIENT_SECRET)
    headers = {'Accept': 'application/json', 'Content-type': 'application/x-www-form-urlencoded',
               'Authorization': auth_header}
    payload = {
        'code': auth_code,
        'redirect_uri': settings.REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    r = requests.post(token_endpoint, data=payload, headers=headers)
    if r.status_code != 200:
        return r.text
    bearer_raw = json.loads(r.text)

    if 'id_token' in bearer_raw:
        id_token = bearer_raw['id_token']
    else:
        id_token = None

    return Bearer(bearer_raw['x_refresh_token_expires_in'], bearer_raw['access_token'], bearer_raw['token_type'],
                  bearer_raw['refresh_token'], bearer_raw['expires_in'], id_token=id_token)


def get_bearer_token_from_refresh_token(refresh_token):
    discovery_document = QuickBooksDiscoveryDocument.objects.first()
    token_endpoint = discovery_document.token_endpoint
    auth_header = 'Basic ' + string_to_base64(settings.CLIENT_ID + ':' + settings.CLIENT_SECRET)
    headers = {'Accept': 'application/json', 'Content-type': 'application/x-www-form-urlencoded',
               'Authorization': auth_header}
    payload = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    r = requests.post(token_endpoint, data=payload, headers=headers)
    bearer_raw = json.loads(r.text)

    if 'id_token' in bearer_raw:
        id_token = bearer_raw['id_token']
    else:
        id_token = None

    return Bearer(bearer_raw['x_refresh_token_expires_in'], bearer_raw['access_token'], bearer_raw['token_type'],
                  bearer_raw['refresh_token'], bearer_raw['expires_in'], id_token=id_token)


def revoke_token(token):
    discovery_document = QuickBooksDiscoveryDocument.objects.first()
    revoke_endpoint = discovery_document.revocation_endpoint
    auth_header = 'Basic ' + string_to_base64(settings.CLIENT_ID + ':' + settings.CLIENT_SECRET)
    headers = {'Accept': 'application/json', 'content-type': 'application/json', 'Authorization': auth_header}
    payload = {'token': token}
    r = requests.post(revoke_endpoint, json=payload, headers=headers)

    if r.status_code >= 500:
        return 'internal_server_error'
    elif r.status_code >= 400:
        return 'Token is incorrect.'
    else:
        return 'Revoke successful'


def get_company_info(access_token, realm_id):
    route = '/v3/company/{0}/companyinfo/{0}'.format(realm_id)
    auth_header = 'Bearer ' + access_token
    headers = {'Authorization': auth_header, 'Accept': 'application/json'}
    r = requests.get(settings.SANDBOX_QBO_BASEURL + route, headers=headers)
    status_code = r.status_code
    if status_code == 200:
        response = json.loads(r.text)
        return response, status_code
    else:
        response = ''
        return response, status_code


def string_to_base64(s):
    return base64.b64encode(bytes(s, 'utf-8')).decode()


# Returns a securely generated random string. Source from the django.utils.crypto module.
def get_random_string(length,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    return ''.join(random.choice(allowed_chars) for i in range(length))


# Create a random secret key. Source from the django.utils.crypto module.
def get_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return get_random_string(40, chars)
