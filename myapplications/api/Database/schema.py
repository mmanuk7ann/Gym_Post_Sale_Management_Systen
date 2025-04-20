from typing import List, Optional
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, EmailStr


# --- Gym Schemas ---

class GymBase(BaseModel):
    name: str
    username: str
    address: Optional[str] = None
    phone: Optional[str] = None

class GymCreate(GymBase):
    ...

class GymUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class GymOut(GymBase):
    gym_id: int

    class Config:
        orm_mode = True


# --- Package Schemas ---

class PackageBase(BaseModel):
    name: str
    duration_months: int
    price: Decimal
    description: Optional[str] = None

class PackageCreate(PackageBase):
    gym_id: int

class PackageUpdate(BaseModel):
    name: Optional[str] = None
    duration_months: Optional[int] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None

class PackageOut(PackageBase):
    package_id: int
    gym_id: int

    class Config:
        orm_mode = True