from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from Database.database import get_db

from crud import get_customers_for_gym, get_risk_customers_for_gym
from Database.schemas import CustomerOut, RiskCustomerOut

router = APIRouter(prefix="/customers", tags=["customers"])

# @router.get("/customer/all", response_model=List[CustomerOut])
# def list_customers(
#     gym_id: int,
#     db: Session = Depends(get_db)
# ):
#     rows = get_customers_for_gym(db, gym_id)
#     return rows

@router.get("/customer/all", response_model=List[CustomerOut])
def list_customers(
    gym_id: int,
    db: Session = Depends(get_db)
):
    customers = get_customers_for_gym(db, gym_id)

    if not customers:
        raise HTTPException(status_code=404, detail="Gym not found")

    out: List[CustomerOut] = []
    for c in customers:
        out.append(CustomerOut(
            name=c.name,
            email=c.email,
            phone=c.phone,
            gender=c.gender,
            membership=c.package.name if c.package else None
        ))
    return out

@router.get("/customer/risk", response_model=List[RiskCustomerOut])
def list_risk_customers(
        gym_id: int,
        db: Session = Depends(get_db),
):
    rows = get_risk_customers_for_gym(db, gym_id)
    return rows

