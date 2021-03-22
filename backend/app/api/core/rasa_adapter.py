""" The RasaAdapter processes a text and returns the corresponding text answer.

To do that, it uses requests to send petitions to a rasa server.
"""
import requests

from api.core.config import settings


class RasaAdapter:
    def __init__(self):
        self.loop = None

        self.client = requests.Session()
        self.base_url = settings.RASA_API_BASE_URL
        self._test_connection()

    def _test_connection(self):
        if not self.client.get(f"{self.base_url}/status"):
            raise Exception(
                "Rasa is not available, check the Rasa configuration")

    def process(self, message, user):
        """ Generates a text response from an user message.

        The method calls our Rasa backend to understand the message and 
        return a correct responses
        """
        # TODO: Generate some kind of user tracker/session to improve the responses from rasa core
        metadata = self.client.get(
            f"{self.base_url}/model/parse", data={"text": message}).json()

        response = self.client.get(
            f"{self.base_url}/webhooks/rest/webhook", data={"sender": user, "message": message}).json()

        return (metadata, response)

rasa = RasaAdapter()
