import urllib
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.conf import settings
from .models import QuickBooksToken, QuickBooksDiscoveryDocument
from .utils import (
    create_user,
    create_invoice,
    invoice_payment,
    get_discovery_document,
    get_bearer_token,
    get_user_profile,
    get_bearer_token_from_refresh_token,
    revoke_token, get_company_info,
    get_secret_key
)


def index(request):
    if request.user.is_authenticated():
        if request.user.is_superuser is True:
            return render(request, 'quickbooks/index.html')

    return HttpResponseForbidden("You don't have access to this page!")


def connect_to_quickbooks(request):
    create_discovery_document = get_discovery_document()
    discovery_document = QuickBooksDiscoveryDocument.objects.first()
    url = discovery_document.authorization_endpoint
    params = {
        'scope': settings.ACCOUNTING_SCOPE,
        'redirect_uri': settings.REDIRECT_URI,
        'response_type': 'code',
        'state': get_csrf_token(request),
        'client_id': settings.CLIENT_ID
    }
    url += '?' + urllib.parse.urlencode(params)

    return redirect(url)


def auth_code_handler(request):
    state = request.GET.get('state', None)
    error = request.GET.get('error', None)
    if error == 'access_denied':
        return redirect('index')
    if state is None:
        return HttpResponseBadRequest()
    elif state != get_csrf_token(request):  # validate against CSRF attacks
        return HttpResponse('unauthorized', status=401)

    auth_code = request.GET.get('code', None)
    if auth_code is None:
        return HttpResponseBadRequest()

    bearer = get_bearer_token(auth_code)
    realm_id = request.GET.get('realmId', None)
    update_session(request, bearer.access_token, bearer.refresh_token, realm_id)
    query = QuickBooksToken.objects.first()
    if not query:
        create = QuickBooksToken.objects.create(
            quickbooks_realm_id=realm_id,
            quickbooks_access_token=bearer.access_token,
            quickbooks_access_token_expires_in=bearer.access_token_expire,
            quickbooks_access_token_updated=timezone.now(),
            quickbooks_refresh_token=bearer.refresh_token,
            quickbooks_refresh_token_expires_in=bearer.refresh_token_expire,
            quickbooks_refresh_token_updated=timezone.now()
        )
    else:
        update = QuickBooksToken.objects.update(
            quickbooks_realm_id=realm_id,
            quickbooks_access_token=bearer.access_token,
            quickbooks_access_token_expires_in=bearer.access_token_expire,
            quickbooks_access_token_updated=timezone.now(),
            quickbooks_refresh_token=bearer.refresh_token,
            quickbooks_refresh_token_expires_in=bearer.refresh_token_expire,
            quickbooks_refresh_token_updated=timezone.now()
        )

    return redirect('connected')


def connected(request):
    query = QuickBooksToken.objects.first()
    access_token = query.quickbooks_access_token

    if access_token is None:
        return HttpResponse('Your Bearer token has expired, please initiate connect to QuickBooks again')

    refresh_token = query.quickbooks_refresh_token

    realm_id = query.quickbooks_realm_id
    if realm_id is None:
        user_profile_response, status_code = get_user_profile(access_token)

        if status_code >= 400:
            # if call to User Profile Service doesn't succeed then get a new bearer token from refresh token and try again
            bearer = get_bearer_token_from_refresh_token(refresh_token)
            query = QuickBooksToken.objects.update(
                quickbooks_realm_id=realm_id,
                quickbooks_access_token=bearer.access_token,
                quickbooks_access_token_expires_in=bearer.access_token_expire,
                quickbooks_access_token_updated=timezone.now(),
                quickbooks_refresh_token=bearer.refresh_token,
                quickbooks_refresh_token_expires_in=bearer.refresh_token_expire,
                quickbooks_refresh_token_updated=timezone.now()
            )
            user_profile_response, status_code = get_user_profile(bearer.access_token)
            update_session(request, bearer.access_token, bearer.refresh_token, realm_id)

            if status_code >= 400:
                return HttpResponseServerError()
        c = {
            'first_name': user_profile_response.get('givenName', ' '),
        }
    else:
        if request.session.get('name') is None:
            name = ''
        else:
            name = request.session.get('name')
        c = {
            'first_name': name,
        }

    return render(request, 'quickbooks/connected.html', context=c)


def disconnect(request):
    query = QuickBooksToken.objects.first()
    access_token = query.quickbooks_access_token
    refresh_token = query.quickbooks_refresh_token

    revoke_response = ''
    if not access_token is None:
        revoke_response = revoke_token(access_token)
    elif not refresh_token is None:
        revoke_response = revoke_token(refresh_token)
    else:
        return HttpResponse('No accessToken or refreshToken found, Please connect again')

    # request.session.flush()
    return HttpResponse(revoke_response)


def refresh_token_call(request):
    query = QuickBooksToken.objects.first()
    refresh_token = query.quickbooks_refresh_token

    if refresh_token is None:
        return HttpResponse('Not authorized')

    bearer = get_bearer_token_from_refresh_token(refresh_token)
    query = QuickBooksToken.objects.update(
        quickbooks_access_token=bearer.access_token,
        quickbooks_access_token_expires_in=bearer.access_token_expire,
        quickbooks_access_token_updated=timezone.now(),
        quickbooks_refresh_token=bearer.refresh_token,
        quickbooks_refresh_token_expires_in=bearer.refresh_token_expire,
        quickbooks_refresh_token_updated=timezone.now()
    )
    if isinstance(bearer, str):
        return HttpResponse(bearer)
    else:
        return HttpResponse('Access Token: ' + bearer.access_token + ', Refresh Token: ' + bearer.refresh_token)


def api_call(request):
    query = QuickBooksToken.objects.first()
    access_token = query.quickbooks_access_token

    if access_token is None:
        return HttpResponse('Your Bearer token has expired, please initiate C2QB flow again')

    realm_id = query.quickbooks_realm_id
    if realm_id is None:
        return HttpResponse('No realm ID. QBO calls only work if the accounting scope was passed!')

    refresh_token = query.quickbooks_refresh_token

    company_info_response, status_code = get_company_info(access_token, realm_id)

    # todo check all statuses
    if status_code >= 400:
        # if call to QBO doesn't succeed then get a new bearer token from refresh token and try again
        bearer = get_bearer_token_from_refresh_token(refresh_token)
        update_session(request, bearer.access_token, bearer.refresh_token, realm_id)
        query = QuickBooksToken.objects.update(
            quickbooks_access_token=bearer.access_token,
            quickbooks_access_token_expires_in=bearer.access_token_expire,
            quickbooks_access_token_updated=timezone.now(),
            quickbooks_refresh_token=bearer.refresh_token,
            quickbooks_refresh_token_expires_in=bearer.refresh_token_expire,
            quickbooks_refresh_token_updated=timezone.now()
        )
        company_info_response, status_code = get_company_info(bearer.access_token, realm_id)

        if status_code >= 400:
            return HttpResponseServerError()

    # create_user_response, status_code = create_user(access_token, realm_id)
    # customer_id = create_user_response['Customer']['Id']
    #
    # create_invoice_response, status_code = create_invoice(access_token, realm_id, customer_id)
    # invoice_id = create_invoice_response['Invoice']['Id']
    # invoice_amount = create_invoice_response['Invoice']['TotalAmt']
    #
    # invoice_payment_response, status_code = invoice_payment(access_token, realm_id, customer_id, invoice_id,
    #                                                         invoice_amount)
    company_name = company_info_response['CompanyInfo']['CompanyName']
    address = company_info_response['CompanyInfo']['CompanyAddr']
    return HttpResponse('Company Name: ' + company_name + ', Company Address: ' + address['Line1'] + ', ' + address[
        'City'] + ', ' + ' ' + address['PostalCode'])


def get_csrf_token(request):
    token = request.session.get('csrfToken', None)
    if token is None:
        token = get_secret_key()
        request.session['csrfToken'] = token
    return token


def update_session(request, access_token, refresh_token, realm_id):
    request.session['accessToken'] = access_token
    request.session['refreshToken'] = refresh_token
    request.session['realmId'] = realm_id
