"""
data_generator.py

This module uses the Faker library to generate synthetic data for a gym membership database.
It includes generators for gyms, packages, customers, transactions, and attendance records.
"""

from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# ----- Gyms -----
def generate_gym(gym_id):
    """
    Generate a fake gym record.

    Args:
        gym_id (int): Unique ID for the gym.

    Returns:
        dict: A dictionary representing a gym.
    """
    return {
        "gym_id": gym_id,
        "name": fake.company(),
        "username": fake.user_name(),
        "address": fake.address(),
        "phone": fake.phone_number()
    }

# ----- Packages -----
def generate_package(package_id, gym_id):
    """
    Generate a fake package record.

    Args:
        package_id (int): Unique ID for the package.
        gym_id (int): ID of the gym offering the package.

    Returns:
        dict: A dictionary representing a gym package.
    """
    return {
        "package_id": package_id,
        "gym_id": gym_id,
        "name": fake.word().capitalize() + " Package",
        "duration_months": random.choice([1, 3, 6, 12]),
        "price": round(random.uniform(30.0, 300.0), 2),
        "description": fake.sentence()
    }

# ----- Customers -----
def generate_customer(customer_id, gym_id, package_id):
    """
    Generate a fake customer record.

    Args:
        customer_id (int): Unique ID for the customer.
        gym_id (int): ID of the gym the customer belongs to.
        package_id (int): ID of the package the customer is subscribed to.

    Returns:
        dict: A dictionary representing a customer.
    """
    return {
        "customer_id": customer_id,
        "gym_id": gym_id,
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=60),
        "gender": random.choice(["Male", "Female", "Other"]),
        "join_date": fake.date_between(start_date='-2y', end_date='today'),
        "status": random.choice(["active", "inactive"]),
        "package_id": package_id,
        "trainer_id": random.randint(1, 10)  # Dummy trainer ID
    }

# ----- Transactions -----
def generate_transaction(transaction_id, customer_id):
    """
    Generate a fake transaction record.

    Args:
        transaction_id (int): Unique ID for the transaction.
        customer_id (int): ID of the customer who made the transaction.

    Returns:
        dict: A dictionary representing a transaction.
    """
    return {
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "amount": random.randint(30, 300),
        "date": fake.date_between(start_date='-2y', end_date='today')
    }

# ----- Attendance -----
def generate_attendance(attendance_id, customer_id):
    """
    Generate a fake attendance record.

    Args:
        attendance_id (int): Unique ID for the attendance session.
        customer_id (int): ID of the customer who attended.

    Returns:
        dict: A dictionary representing an attendance record with check-in and check-out times.
    """
    check_in = fake.date_time_between(start_date='-1y', end_date='now')
    check_out = check_in + timedelta(hours=random.randint(1, 3))

    return {
        "attendance_id": attendance_id,
        "customer_id": customer_id,
        "check_in": check_in,
        "check_out": check_out
    }
