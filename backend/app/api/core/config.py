""" Settings singleton that gets autocompleted from env vars """
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Service ABC"
    PROJECT_DESCRIPTION: str = "Subscribe to sms notifications from our service"
    SECRET_KEY: str = "a509410918f4c0d828b7c68a49007adee1bfede7600475a0adc9565974eb2773"
    HASHING_ALGORITHM: str = "HS256"
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DEMO_USERNAME: str = "spicy"
    DEMO_USER_PASSWORD: str = "soup"

    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str

    RASA_API_BASE_URL: str = "http://rasa:5005"

    MONGO_BASE_HOST_PORT: str = "mongo:27017"
    MONGO_USERNAME: str
    MONGO_PASSWORD: str

    class Config:
        case_sensitive = True


settings = Settings()