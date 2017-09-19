import stripe

from django.conf import settings
# from .models import StripePlanNames

# API KEY and Personal URL for Active Campaign Account
STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC_KEY
STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY


# Function to generate stripe plan id and name
def generate_plan_name(trip, payments, price):
    trip2 = trip
    trip_for_name = trip.replace('.', '-')
    trip_lowercase = trip2.lower().replace(' ', '-')
    plan_id = '%s-%s-%s' % (trip_lowercase, payments, price)
    plan_name = '%s - %s - %s' % (trip_for_name, payments, price)
    plan = (plan_id, plan_name)
    return plan
