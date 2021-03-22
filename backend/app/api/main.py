from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import asyncio

from api.auth import auth
from api.routes import subscriptions
from api.core.config import settings
from api.core.message_listener import message_listener
from api.core.message_handler import message_handler


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION
)

@app.on_event("startup")
async def startup_event():
    """ Startup functionality """
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, message_listener.start)
    loop.run_in_executor(None, message_handler.start)

# Redirect all the Validation Errors from FastApi from 422 to 400
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": "Validation error"})

# Load API routes to FastAPI app
app.include_router(auth.router, tags=["auth"])
app.include_router(subscriptions.router, tags=["subscriptions"])
