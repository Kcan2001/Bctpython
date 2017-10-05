from __future__ import absolute_import, unicode_literals
from celery import Celery
import raven
from raven.contrib.celery import register_signal, register_logger_signal
import os


class Celery(Celery):
    def on_configure(self):
        client = raven.Client(
            'http://da385935ce644993bc71402cf42a45aa:f12c65a8409e40eb8158350f274f193a@sentry.milosolutions.com/64')

        # register a custom filter to filter out duplicate logs
        register_logger_signal(client)

        # hook into the Celery error handler
        register_signal(client)


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bctpython.settings')

app = Celery('Bctpython')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
