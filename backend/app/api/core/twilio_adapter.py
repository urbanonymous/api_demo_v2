""" The TwilioAdapter processes a text and returns the corresponding text answer.

To do that, it uses requests to send petitions to a twilio server.
"""
from twilio.rest import Client
from functools import partial

import threading
import requests

from api.core.config import settings


class TwilioAdapter:
    def __init__(self):
        self.phone_number = settings.TWILIO_PHONE_NUMBER
        self.client = Client(settings.TWILIO_ACCOUNT_SID,
                             settings.TWILIO_AUTH_TOKEN)

        self.delayed_messages = []

    def get_messages(self):
        return self.client.messages.list(to=self.phone_number)

    def send_message(self, message, target, delay: float = None):
        if delay:
            self.delayed_messages.append(threading.Timer(delay, self.send_message, args=[message, target]).start())
        else:
            message = self.client.messages \
                .create(
                    body=message,
                    from_=self.phone_number,
                    to=target
                )
            return message


twilio = TwilioAdapter()
