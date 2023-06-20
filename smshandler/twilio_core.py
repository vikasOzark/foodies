# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from django.conf import settings
import json
from dataclasses import dataclass


@dataclass
class TwilioSMSHandler:
    """Create sms object and send vio twilio
    params
    :body
    :to
    :from : (defined in settings)
    """
    body:str
    from_:str
    to:str
    
    def create_sms(self, **kwargs) -> json:
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        message = client.messages.create(
                        body=self.body,
                        from_=self.from_,
                        to=self.to
                    )
        
    def send(self) ->set :
        """return set(sid, json)"""
        response = self.create_sms()
        return (response.sid, response.text)
