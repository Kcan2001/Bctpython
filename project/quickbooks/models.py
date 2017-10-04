from django.db import models


class Bearer:
    def __init__(self, refresh_token_expire, access_token, token_type, refresh_token, access_token_expire,
                 id_token=None):
        self.token_type = token_type
        self.access_token = access_token
        self.access_token_expire = access_token_expire
        self.refresh_token = refresh_token
        self.refresh_token_expire = refresh_token_expire
        self.id_token = id_token


class QuickBooksToken(models.Model):
    quickbooks_realm_id = models.IntegerField(null=True)
    quickbooks_access_token = models.CharField(max_length=1000, null=True)
    quickbooks_access_token_expires_in = models.PositiveIntegerField(null=True)
    quickbooks_access_token_updated = models.DateTimeField(null=True)
    quickbooks_refresh_token = models.CharField(max_length=100, null=True)
    quickbooks_refresh_token_expires_in = models.PositiveIntegerField(null=True)
    quickbooks_refresh_token_updated = models.DateTimeField(null=True)


class QuickBooksDiscoveryDocument(models.Model):
    issuer = models.CharField(max_length=100, null=True)
    authorization_endpoint = models.CharField(max_length=100, null=True)
    token_endpoint = models.CharField(max_length=100, null=True)
    userinfo_endpoint = models.CharField(max_length=100, null=True)
    revocation_endpoint = models.CharField(max_length=100, null=True)
    jwks_uri = models.CharField(max_length=100, null=True)


class QuickBooksErrorRequest(models.Model):
    CUSTOMER = 'C'
    INVOICE = 'I'
    PAYMENT = 'P'
    REQUEST_TYPE_CHOICES = (
        (CUSTOMER, 'Customer'),
        (INVOICE, 'Invoice'),
        (PAYMENT, 'Payment'),
    )
    request_type = models.CharField(max_length=1, choices=REQUEST_TYPE_CHOICES, null=True)
    request_body = models.CharField(max_length=1000, null=True)
    request_headers = models.CharField(max_length=1000, null=True)
    request_url = models.CharField(max_length=1000, null=True)
    status_code = models.PositiveSmallIntegerField(null=True)
    response_text = models.CharField(max_length=2000, null=True)
    successful = models.BooleanField(default=False)
