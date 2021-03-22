""" The message listener singleton acts as a middleware between twilio and our API.

Initially it allows to read from only one phone number.

As this demo must run as is, without extensive user input/configuration, the message listener will
use a polling approach to Twilio instead of subscribing to events using a webhook.
"""
import time
import threading

from api.core.config import settings
from api.core.message_handler import message_handler
from api.core.twilio_adapter import twilio


class MessageListener:
    def __init__(self):
        self.thread = threading.Thread(target=self.run, name="MessageListener")

        self.messages = {}

        # State flags
        self.started = False
        self.running = False
        self.ready = False

    def start(self):
        """ Starts the thread of the message listener class"""
        if not self.started:
            self.thread.start()
            self.started = True

    def run(self):
        """Polling sms for the required phone from twilio"""
        self.running = True
        while self.running:
            messages = twilio.get_messages()
            for message in messages:
                if message.sid not in self.messages.keys():
                    # Save the importan
                    message_data = {
                        "sid": message.sid,
                        "body": message.body,
                        "from_": message.from_
                    }
                    self.messages[message.sid] = message_data
                    if self.ready:
                        message_handler.queue.put(message_data)

            # Indicate that the first iteration was completed
            if not self.ready:
                self.ready = True

            time.sleep(2)

    def stop(self):
        self.running = False


message_listener = MessageListener()
