from pydantic import BaseModel

class TwilioIncomingMessage(BaseModel):
    text: str

class TwilioOutgoingMessage(BaseModel):
    text: str