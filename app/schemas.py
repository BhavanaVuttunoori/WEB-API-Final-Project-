from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from app.models import OperationType


# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6, max_length=100)


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# Calculation Schemas
class CalculationBase(BaseModel):
    operation: OperationType
    operand1: float
    operand2: float


class CalculationCreate(CalculationBase):
    @validator('operand2')
    def validate_division(cls, v, values):
        if 'operation' in values and values['operation'] == OperationType.DIVIDE and v == 0:
            raise ValueError('Cannot divide by zero')
        if 'operation' in values and values['operation'] == OperationType.MODULO and v == 0:
            raise ValueError('Cannot perform modulo by zero')
        return v


class CalculationUpdate(BaseModel):
    operation: Optional[OperationType] = None
    operand1: Optional[float] = None
    operand2: Optional[float] = None


class CalculationResponse(CalculationBase):
    id: int
    user_id: int
    result: float
    created_at: datetime

    class Config:
        from_attributes = True


# History and Statistics Schemas
class CalculationHistory(BaseModel):
    calculations: List[CalculationResponse]
    total_count: int


class UserStatistics(BaseModel):
    total_calculations: int
    calculations_by_operation: dict
    average_result: float
    most_used_operation: Optional[str]
    recent_calculations: List[CalculationResponse]

    class Config:
        from_attributes = True


# Message Response
class Message(BaseModel):
    message: str
