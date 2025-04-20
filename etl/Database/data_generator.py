from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# ----- Gyms -----
def generate_gym(gym_id):
    return {
        "gym_id": gym_id,
        "name": fake.company(),
        "username": fake.user_name(),
        "address": fake.address(),
        "phone": fake.phone_number()
    }

# ----- Packages -----
def generate_package(package_id, gym_id):
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
    return {
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "amount": random.randint(30, 300),
        "date": fake.date_between(start_date='-2y', end_date='today')
    }

# ----- Attendance -----
def generate_attendance(attendance_id, customer_id):
    check_in = fake.date_time_between(start_date='-1y', end_date='now')
    check_out = check_in + timedelta(hours=random.randint(1, 3))

    return {
        "attendance_id": attendance_id,
        "customer_id": customer_id,
        "check_in": check_in,
        "check_out": check_out
    }
