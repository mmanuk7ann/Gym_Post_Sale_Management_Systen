from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Database.database import get_db
from crud import get_member_count, get_average_clv, get_customers_by_package, get_risk_customer_count_for_gym, count_recent_customers
from Database.schemas import CountResponse
from Database.schemas import AverageCLVResponse
from Database.schemas import PackageCustomerSumListResponse, PackageCustomerSumResponse

router = APIRouter(prefix="/gyms", tags=["gyms"])

@router.get("/gym/members-count", response_model=CountResponse)
def total_members(
        gym_id: int,
        db: Session = Depends(get_db),
):
    count = get_member_count(db, gym_id)
    return {"total_members": count}


@router.get("/gym/average-clv", response_model=AverageCLVResponse)
def average_clv(
        gym_id : int,
        db: Session = Depends(get_db),
):
    """
    Get the average CLV (Customer Lifetime Value) for all customers of the current gym.

    :param db: Database session
    :param gym: Current gym object (from authentication)
    :return: Average CLV response
    """
    average_clv_value = get_average_clv(db, gym_id)
    return AverageCLVResponse(average_clv=average_clv_value)


@router.get("/gym/customers-by-package", response_model=PackageCustomerSumListResponse)
def customers_by_package(
        gym_id : int,
        db: Session = Depends(get_db),
):
    package_counts = get_customers_by_package(db, gym_id)

    return PackageCustomerSumListResponse(
        package_counts=package_counts,
    )


@router.get("/gym/risk-count", response_model=int)
def count_risk_customers(
        gym_id: int,
        db: Session = Depends(get_db),
):
    # Get the count of 'At Risk' customers for the current gym
    count = get_risk_customer_count_for_gym(db, gym_id)
    return count



@router.get("/gym/last_week_visits", response_model=int)
def last_week_visits(
        gym_id: int,
        db: Session = Depends(get_db),
):
    count = count_recent_customers(db, gym_id)
    if count is None:
        # just in case something went wrong
        raise HTTPException(status_code=404, detail="Gym not found or no data")
    return count