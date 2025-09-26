from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class ForgotPasswordRequest (SQLModel, table=True):
    __tablename__ = "forgot_password_tokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    token: str = Field(unique=True, index=True)
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)