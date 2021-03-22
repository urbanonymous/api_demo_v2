from pydantic import BaseModel

class User(BaseModel):
    user_id: str

class UserInDB(BaseModel):
    password: str
