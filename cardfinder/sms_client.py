import os
from twilio.rest import Client

from .config import TWILIO_SID, TWILIO_TOKEN, TWILIO_NUMBER
class SMSClient:
    def __init__(self):
        self._client = self.get_client()

    def get_client(self):
        return Client(
            TWILIO_SID,
            TWILIO_TOKEN,
        )

    def send_sms(self, number, message):
       return self._client.messages.create(
            body=message,
            from_=TWILIO_NUMBER,
            to=number
        )
