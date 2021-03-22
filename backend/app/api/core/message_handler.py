""" The message_handler process new massages from the source (Twilio), gets a respose from the rasa adapter
and finally sends an sms answer to the client.

This handler should be refactored to a 'Chain of Responsability'
"""
from queue import SimpleQueue

import time
import threading

from api.core.config import settings
from api.core.twilio_adapter import twilio
from api.core.rasa_adapter import rasa


class MessageHandler:
    def __init__(self):
        self.thread = threading.Thread(target=self.run, name="MessageListener")

        self.queue = SimpleQueue()  # Queue of messages to process

        # State flags
        self.running = False
        self.started = False

    def start(self):
        """ Starts the thread of the message listener class"""
        if not self.started:
            self.thread.start()
            self.started = True

    def run(self):
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
        # Send the text message to Rasa to process it and get the NLU info and text response back
        metadata, response = rasa.process(message["body"], message["from_"])
        print(metadata, response)

        # TODO: Add a command router and commands to handle the intents from the NLU instead of IFs
        message_1 = "We have our service ABC unstable. There is already an ongoing team solving the issue. More info soon."
        message_2 = "The issue with the service ABC had been solved"

        # Send an sms to the requested phone_number using twilio
        #twilio.send_message(message, target)
        


message_handler = MessageHandler()
