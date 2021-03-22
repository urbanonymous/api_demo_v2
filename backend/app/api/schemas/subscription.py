from pydantic import BaseModel

class SubscriptionBase(BaseModel):
    id: str

class SubscriptionState(SubscriptionBase):
    state: str

