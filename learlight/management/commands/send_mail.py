import logging
import requests

logger = logging.getLogger(__name__)

import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        self.send_mail('mailgun@sandbox87787ac6bd344cae847cd4163e3a20df.mailgun.org',
                       ['rajeshbk042@gmail.com, merlin.george@spericorn.com'],
                       subject='Subject text here', text='testing texttttttttttttttttttttt')

    def send_mail(self, from_address, recipients, subject='', text='', html=''):
        for to_address in recipients:
            api_url = "%s%s/messages" % (settings.MAILGUN_API_URL, settings.MAILGUN_DOMAIN)
            print "api_urlapi_url", api_url
            payload = {
                'from': from_address,
                'to': to_address,
                'subject': subject,
                'text': text,
                'html': html
            }

            response = requests.post(api_url, auth=('api', settings.MAILGUN_API_KEY), data=payload)
            print "response", response.content
            if response.status_code != 200:
                message = "Failed to POST email to Mailgun from %s to %s" % (from_address, to_address)
                logger.error(message)

