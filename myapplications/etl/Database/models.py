"""
models.py

Defines the SQLAlchemy ORM models for the gym analytics platform.
This includes tables for gyms, packages, customers, transactions,
attendance, and customer segmentation (CLV and RFM).
"""

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Gym(Base):
    """
    Represents a gym entity.

    Attributes:
        gym_id (int): Primary key.
        name (str): Name of the gym.
        username (str): Unique username for login or identification.
        address (str): Physical address of the gym.
        phone (str): Contact phone number.
    """
    __tablename__ = 'gyms'

    gym_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    username = Column(String)
    address = Column(String)
    phone = Column(String)
    
    customers = relationship("Customer", back_populates="gym")
    packages = relationship("Package", back_populates="gym")


class Package(Base):
    """
    Represents a gym membership package.

    Attributes:
        package_id (int): Primary key.
        gym_id (int): Foreign key to Gym.
        name (str): Name of the package.
        duration_months (int): Duration of the package in months.
        price (Decimal): Price of the package.
        description (str): Description of the package.
    """
    __tablename__ = 'packages'

    package_id = Column(Integer, primary_key=True)
    gym_id = Column(Integer, ForeignKey('gyms.gym_id'))
    name = Column(String)
    duration_months = Column(Integer)
    price = Column(DECIMAL)
    description = Column(String)

    gym = relationship("Gym", back_populates="packages")
    customers = relationship("Customer", back_populates="package")


class Customer(Base):
    """
    Represents a gym customer.

    Attributes:
        customer_id (int): Primary key.
        gym_id (int): Foreign key to Gym.
        name (str): Full name of the customer.
        email (str): Email address.
        phone (str): Phone number.
        birth_date (date): Date of birth.
        gender (str): Gender of the customer.
        join_date (date): Date the customer joined.
        status (str): Status of the membership (e.g., active/inactive).
        package_id (int): Foreign key to Package.
        trainer_id (int): Placeholder ID for assigned trainer.
    """
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True)
    gym_id = Column(Integer, ForeignKey('gyms.gym_id'))
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    birth_date = Column(Date)
    gender = Column(String)
    join_date = Column(Date)
    status = Column(String)
    package_id = Column(Integer, ForeignKey('packages.package_id'))
    trainer_id = Column(Integer)

    gym = relationship("Gym", back_populates="customers")
    package = relationship("Package", back_populates="customers")
    transactions = relationship("Transaction", back_populates="customer")
    attendance_records = relationship("Attendance", back_populates="customer")
    clv_record = relationship("CLV", uselist=False, back_populates="customer")
    rfm_record = relationship("RFM", uselist=False, back_populates="customer")


class Transaction(Base):
    """
    Represents a customer's payment transaction.

    Attributes:
        transaction_id (int): Primary key.
        customer_id (int): Foreign key to Customer.
        amount (int): Transaction amount.
        date (date): Date of the transaction.
    """
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    amount = Column(Integer)
    date = Column(Date)

    customer = relationship("Customer", back_populates="transactions")


class Attendance(Base):
    """
    Represents a gym attendance record.

    Attributes:
        attendance_id (int): Primary key.
        customer_id (int): Foreign key to Customer.
        check_in (datetime): Check-in time.
        check_out (datetime): Check-out time.
    """
    __tablename__ = 'attendance'

    attendance_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    check_in = Column(DateTime)
    check_out = Column(DateTime)

    customer = relationship("Customer", back_populates="attendance_records")


class CLV(Base):
    """
    Represents Customer Lifetime Value (CLV) data.

    Attributes:
        clv_id (int): Primary key.
        customer_id (int): Foreign key to Customer.
        clv_value (Decimal): Predicted customer lifetime value.
        average_order_value (Decimal): Average order value.
        predicted_customer_type (str): Segment label (e.g., 'At Risk', 'Loyalist').
    """
    __tablename__ = 'clv'

    clv_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    clv_value = Column(DECIMAL)
    average_order_value = Column(DECIMAL)
    predicted_customer_type = Column(String)

    customer = relationship("Customer", back_populates="clv_record")


class RFM(Base):
    """
    Represents RFM (Recency, Frequency, Monetary) segmentation data.

    Attributes:
        rfm_id (int): Primary key.
        customer_id (int): Foreign key to Customer.
        recency_score (int): Days since last activity.
        frequency_score (int): Frequency score.
        monetary_score (Decimal): Total spending score.
        customer_segment (str): Segment label (e.g., 'High-Value', 'At Risk').
    """
    __tablename__ = 'rfm'

    rfm_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    recency_score = Column(Integer)
    frequency_score = Column(Integer)
    monetary_score = Column(DECIMAL)  # Fixed typo from 'mointory_score'
    customer_segment = Column(String)

    customer = relationship("Customer", back_populates="rfm_record")