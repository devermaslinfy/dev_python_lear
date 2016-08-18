import logging
import requests

from django.conf import settings


logger = logging.getLogger(__name__)


def send_mail(from_address, recipients, subject='', text='', html=''):
    for to_address in recipients:
        api_url = "%s%s/messages" % (settings.MAILGUN_API_URL, settings.MAILGUN_DOMAIN)
        payload = {
            'from': from_address,
            'to': to_address,
            'subject': subject,
            'text': text,
            'html': html
        }

        response = requests.post(api_url, auth=(settings.MAILGUN_API_USER, settings.MAILGUN_API_KEY), data=payload)

        if response.status_code != 200:
            message = "Failed to POST email to Mailgun from %s to %s" % (from_address, to_address)
            logger.error(message)
