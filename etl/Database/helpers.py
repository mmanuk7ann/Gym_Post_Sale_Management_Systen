from sqlalchemy.orm import Session
from sqlalchemy import func
from Database.models import Customer, Gym, Transaction, Attendance

def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()

def get_gym_customers(db: Session, gym_id: int):
    return db.query(Customer).filter(Customer.gym_id == gym_id).all()

def get_total_revenue(db: Session):
    return db.query(func.sum(Transaction.amount)).scalar()

def get_active_customers(db: Session):
    return db.query(Customer).filter(Customer.status == "active").all()

def get_attendance_between_dates(db: Session, start_date, end_date):
    return db.query(Attendance).filter(Attendance.check_in >= start_date, Attendance.check_out <= end_date).all()

