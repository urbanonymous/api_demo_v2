""" The message_handler process new massages from the source (Twilio), gets a respose from the rasa adapter
and finally sends an sms answer to the client.

This handler should be refactored to a 'Chain of Responsability'
"""
from queue import SimpleQueue

import time

from api.core.config import settings
from api.core.twilio_adapter import twilio
from api.core.rasa_adapter import rasa


class MessageHandler:
    def __init__(self):
        self.loop = None

        # State flags
        self.running = False

        self.queue = SimpleQueue()  # Queue of messages to process

    def start(self):
        self.running = True
        while self.running:
            message = None
            try:
                message = self.queue.get()
                
            except Exception:
                # Empty Queue, ignore
                pass

            if message:
                self.handle_message(message)
            time.sleep(1)

    def stop(self):
        self.running = False


    def handle_message(self, message):
        print(message)
        # Decompose the message into usefull parts
        user = message.user
        target = "test"
        # Send the text message to Rasa to process it and get the NLU info and text response back
        metadata, response = rasa.process(message, user)

        # Send an sms to the requested phone_number using twilio
        #twilio.send_message(message, target)
        print(message, target)


message_handler = MessageHandler()
