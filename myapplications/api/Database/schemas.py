from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, EmailStr

# --- Base Schemas ---

class BaseGym(BaseModel):
    name: str
    username: str
    address: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        orm_mode = True

class BasePackage(BaseModel):
    name: str
    duration_months: int
    price: Decimal
    description: Optional[str] = None

    class Config:
        orm_mode = True

class BaseCustomer(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    membership: Optional[str] = None
    gender: Optional[str] = None

    class Config:
        orm_mode = True


# --- Gym Schemas ---

class GymCreate(BaseGym):
    email: EmailStr
    password: str

class GymUpdate(BaseGym):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class GymOut(BaseGym):
    gym_id: int


# --- Package Schemas ---

class PackageCreate(BasePackage):
    gym_id: int

class PackageUpdate(BasePackage):
    name: Optional[str] = None
    duration_months: Optional[int] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None

class PackageOut(BasePackage):
    package_id: int
    gym_id: int


# --- Auth / Token Schemas ---

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    gym_id: Optional[int] = None


# --- Customer Schemas ---

class CustomerOut(BaseCustomer):
    pass


# --- Email Schemas ---

class EmailSend(BaseModel):
    email: EmailStr
    text: str


# --- Response Schemas ---

class CountResponse(BaseModel):
    total_members: int

class AverageCLVResponse(BaseModel):
    average_clv: Decimal

class PackageCustomerSumResponse(BaseModel):
    package_name: str
    total_customers: int

class PackageCustomerSumListResponse(BaseModel):
    packages: List[PackageCustomerSumResponse]


class RiskCustomerOut(BaseModel):
    name: str
    last_visit: date
    membership: str
    inactive_days: int

    class Config:
        orm_mode = True