from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from Database.database import get_db

from dependencies import get_current_gym
from crud import get_customers_for_gym, get_risk_customers_for_gym
from Database.schemas import CustomerOut, RiskCustomerOut

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("/customer/all", response_model=List[CustomerOut])
def list_customers(
    db: Session = Depends(get_db),
    gym = Depends(get_current_gym),
):
    rows = get_customers_for_gym(db, gym.gym_id)
    # rows are tuples → FastAPI will map them to CustomerOut
    return rows


@router.get("/customer/risk", response_model=List[RiskCustomerOut])
def list_risk_customers(
    db: Session = Depends(get_db),
    gym = Depends(get_current_gym),
):
    # Retrieve at risk customers for the current gym
    rows = get_risk_customers_for_gym(db, gym.gym_id)
    return rows

