
from datetime import datetime, timedelta
from typing import Any, Union
from fastapi import APIRouter, Depends, Header, HTTPException, Query, status

from api.schemas.user import User
from api.schemas.subscription import SubscriptionState
from api.core.config import settings
from api.core.twilio_adapter import twilio
from api.auth.deps import get_current_user

router = APIRouter()


@router.get("/run", response_model=SubscriptionState)
async def run_subscription(
    phone_number: str = Query(...,        
        title="Phone Number",
        description="Phone number in E.164 format. e.g. +44123123123"),
    user: User = Depends(get_current_user)
):
    """
    Initiates a subscription to the specified phone number
    """
    # TODO: Add validation to the phone numbers (pydantic + phonenumbers)
    try:
        # TODO: Ideally this endpoint should send the request to 
        # some sort of Subscriptions engine/logic to handle them.
        # TODO: Add a collection of used text messages and validation to those 
        default_message = "You have requested to subscribe for updates for our service ABC. Could you confirm that you want to subscribe for service updates?"
        message = twilio.send_message(default_message, phone_number)
        return SubscriptionState(id=message.sid, state="Pending approval")

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid phone number",
        )

