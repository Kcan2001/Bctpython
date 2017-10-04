from django.conf.urls import url
from .views import index, connect_to_quickbooks, auth_code_handler, disconnect, api_call, connected, refresh_token_call, \
    manual_update_discovery_doc

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^connect-to-quickbooks/?$', connect_to_quickbooks, name='connect_to_quickbooks'),
    url(r'^auth-code-handler/?$', auth_code_handler, name='auth_code_handler'),
    url(r'^disconnect/?$', disconnect, name='disconnect'),
    url(r'^api-call/?$', api_call, name='api_call'),
    url(r'^connected/?$', connected, name='connected'),
    url(r'^discovery/?$', manual_update_discovery_doc, name='get_discovery_document'),
    url(r'^refresh-token-call/?$', refresh_token_call, name='refresh_token_call')
]
