"""
helpers.py

Contains utility functions for querying the gym database using SQLAlchemy.
Includes retrieval functions for customers, revenue, and attendance.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from Database.models import Customer, Gym, Transaction, Attendance

def get_customer_by_id(db: Session, customer_id: int):
    """
    Retrieve a single customer by their ID.

    Args:
        db (Session): SQLAlchemy database session.
        customer_id (int): ID of the customer to retrieve.

    Returns:
        Customer: The customer object if found, else None.
    """
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()

def get_gym_customers(db: Session, gym_id: int):
    """
    Retrieve all customers associated with a specific gym.

    Args:
        db (Session): SQLAlchemy database session.
        gym_id (int): ID of the gym.

    Returns:
        list[Customer]: List of customers belonging to the gym.
    """
    return db.query(Customer).filter(Customer.gym_id == gym_id).all()

def get_total_revenue(db: Session):
    """
    Calculate the total revenue from all transactions.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        float: Sum of all transaction amounts.
    """
    return db.query(func.sum(Transaction.amount)).scalar()

def get_active_customers(db: Session):
    """
    Retrieve all customers who are currently active.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        list[Customer]: List of active customers.
    """
    return db.query(Customer).filter(Customer.status == "active").all()

def get_attendance_between_dates(db: Session, start_date, end_date):
    """
    Retrieve attendance records within a specified date range.

    Args:
        db (Session): SQLAlchemy database session.
        start_date (datetime): Start of the date range.
        end_date (datetime): End of the date range.

    Returns:
        list[Attendance]: List of attendance records matching the date filter.
    """
    return db.query(Attendance).filter(
        Attendance.check_in >= start_date,
        Attendance.check_out <= end_date
    ).all()
