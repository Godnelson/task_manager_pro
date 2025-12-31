import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserPublic(BaseModel):
    id: uuid.UUID
    email: EmailStr
    created_at: datetime
