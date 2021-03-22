from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api.auth import auth
from api.routes import subscriptions
from api.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION
)

# Redirect all the Validation Errors from FastApi from 422 to 400
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": "Validation error"})

# Load API routes to FastAPI app 
app.include_router(auth.router, tags=["auth"])
app.include_router(subscriptions.router, tags=["subscriptions"])
