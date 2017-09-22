# Function to generate stripe plan id and name
def generate_plan_name(trip, payments, price):
    trip_for_name = trip.replace('.', '-')
    trip_lowercase = trip.lower().replace(' ', '-')
    plan_id = '%s-%s-%s' % (trip_lowercase, payments, price)
    plan_name = '%s - %s - %s' % (trip_for_name, payments, price)
    plan = (plan_id, plan_name)
    return plan
