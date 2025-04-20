from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Gym(Base):
    __tablename__ = 'gyms'

    gym_id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    address = Column(String)
    phone = Column(String)

    customers = relationship("Customer", back_populates="gym")
    packages = relationship("Package", back_populates="gym")


class Package(Base):
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


class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    amount = Column(Integer)
    date = Column(Date)

    customer = relationship("Customer", back_populates="transactions")


class Attendance(Base):
    __tablename__ = 'attendance'

    attendance_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    check_in = Column(DateTime)
    check_out = Column(DateTime)

    customer = relationship("Customer", back_populates="attendance_records")
