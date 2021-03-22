from pydantic import BaseModel

class SubscriptionBase(BaseModel):
    id: str

class Subscription(SubscriptionBase):
    state: str

