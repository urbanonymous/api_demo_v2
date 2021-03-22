""" The TwilioAdapter processes a text and returns the corresponding text answer.

To do that, it uses requests to send petitions to a twilio server.
"""
from twilio.rest import Client

import requests

from api.core.config import settings


class TwilioAdapter:
    def __init__(self):
        self.loop = None
        self.phone_number = settings.TWILIO_PHONE_NUMBER
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def get_messages(self):
        return self.client.messages.list(to=self.phone_number)

    def send_message(self, target, message):
        """
        message = client.messages \
            .create(
                body=message,
                from_=self.phone_number
                to=target
            )
        """
        print(message)



twilio = TwilioAdapter()
