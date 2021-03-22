""" The message listener acts as a middleware between twilio and our API.

Initially it allows to read from only one phone number.

As this demo must run as is, without extensive user input/configuration, the message listener will
use a polling approach to Twilio instead of subscribing to events using a webhook.
"""
import time

from api.core.config import settings
from api.core.message_handler import message_handler
from api.core.twilio_adapter import twilio


class MessageListener:
    def __init__(self):
        self.messages = {}

        # State flags
        self.running = False
        self.ready = False

    def start(self):
        self.running = True
        while self.running:
            messages = twilio.get_messages()
            for message in messages:
                if message not in self.messages:
                    if not self.ready:
                        self.messages[message["id"]] = message
                    else:
                        self.messages[message["id"]] = message
                        message_handler.queue.put(message)
            
            # Indicate that the first iteration was completed
            if not self.ready: 
                self.ready = True

            time.sleep(1)

    def stop(self):
        self.running = False
