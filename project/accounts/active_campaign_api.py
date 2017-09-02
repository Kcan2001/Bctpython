from django.conf import settings
import requests

# API KEY and Personal URL for Active Campaign Account
ACTIVECAMPAIGN_URL = settings.ACTIVECAMPAIGN_URL
ACTIVECAMPAIGN_KEY = settings.ACTIVECAMPAIGN_KEY


# Function for making api call to Active Campaign servers
def active_campaign_api_request(url, headers, params, data):
    # We don't want to terminate application if AC server will not response, so:
    try:
        response = requests.request("POST", url=url, params=params, data=data, headers=headers)
        # print(response.json())
        return
    # Just pass is any of known errors will occur:
    except requests.exceptions.RequestException as e:
        pass


'''Available args for API (for details: http://www.activecampaign.com/api/overview.php): 
email - email of the new contact. Example: 'test@example.com'
first_name - first name of the contact. Example: 'FirstName'
last_name - last name of the contact. Example: 'LastName'
phone - phone number of the contact. Example: '+1 312 201 0300'
orgname - organization name (if doesn't exist, this will create a new organization) - MUST HAVE CRM FEATURE FOR THIS.
tags - tags for this contact (comma-separated). Example: "tag1, tag2, etc"
ip4 - IP address of the contact. Example: '127.0.0.1' If not supplied, it will default to '127.0.0.1'
field[345,0] - custom field values. Example: field[345,0] = 'value'. In this example, "345" is the field ID. Leave 0 as is.
field[%PERS_1%,0] - 'value' (You can also use the personalization tag to specify which field you want updated)
p[123]*	- assign to lists. List ID goes in brackets, as well as the value.
status[123] - the status for each list the contact is added to. Examples: 1 = active, 2 = unsubscribed
form - optional subscription Form ID, to inherit those redirection settings. Example: 1001. This will allow you to mimic adding the contact through a subscription form, where you can take advantage of the redirection settings.
noresponders[123]- whether or not to set "do not send any future responders." Examples: 1 = yes, 0 = no.
sdate[123] - subscribe date for particular list - leave out to use current date/time. Example: '2009-12-07 06:00:00'
instantresponders[123] - use only if status = 1. Whether or not to set "send instant responders." Examples: 1 = yes, 0 = no.
lastmessage[123] - whether or not to set "send the last broadcast campaign." Examples: 1 = yes, 0 = no.'''


class ActiveCampaign(object):

    # Add a new contact to the system.
    def add_contact(email, first_name, last_name):
        # API action
        action = 'contact_add'
        params = [
            ('api_action', action),
            ('api_key', ACTIVECAMPAIGN_KEY),
            ('api_output', 'json'),
        ]
        url = '{0}/admin/api.php?api_action={1}'.format(ACTIVECAMPAIGN_URL, action)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = [
            ('email', email),
            ('first_name', first_name),
            ('last_name', last_name),
        ]
        # r = requests.post(url=url, params=params, data=data, headers=headers)
        r = active_campaign_api_request(url, headers, params, data)

    # Add or edit a contact based on their email address. Instead of calling contact_view to check
    # if the contact exists, and then calling contact_add or contact_edit,
    # you can make just one call and include only the information you want added or updated.
    def sync_contact(email, first_name, last_name, tags):
        # Here you can determine your main list id
        list_id = '1'

        # API action
        action = 'contact_sync'
        params = [
            ('api_action', action),
            ('api_key', ACTIVECAMPAIGN_KEY),
            ('api_output', 'json'),
        ]
        url = '{0}/admin/api.php?api_action={1}'.format(ACTIVECAMPAIGN_URL, action)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = [
            ('email', email),
            ('first_name', first_name),
            ('last_name', last_name),
            ('tags', tags),
            ('p[123]', list_id),
        ]
        # r = requests.post(url=url, params=params, data=data, headers=headers)
        r = active_campaign_api_request(url, headers, params, data)
        # print(r)
