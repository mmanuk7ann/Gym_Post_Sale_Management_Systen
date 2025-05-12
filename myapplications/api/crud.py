from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, cast, Date
from sqlalchemy import select
import Database.models as models
import utils.security as sec

# --- Auth / Gym ---
def get_gym_by_email(db: Session, email: str):
    return db.query(models.Gym).filter(models.Gym.email == email).first()

def get_gyms_by_gym_id(db: Session, gym_id: int):
    return db.query(models.Gym).filter(models.Gym.gym_id == gym_id).first()

def create_gym(db: Session, gym_in):
    hashed = sec.hash_password(gym_in.password)
    db_gym = models.Gym(
        name=gym_in.name,
        email=gym_in.email,
        hashed_password=hashed
    )
    db.add(db_gym)
    db.commit()
    db.refresh(db_gym)
    return db_gym

# --- Members count ---
def get_member_count(db: Session, gym_id: int) -> int:
    return db.query(func.count(models.Customer.customer_id))\
             .filter(models.Customer.gym_id == gym_id)\
             .scalar()

# --- Customers list ---
# def get_customers_for_gym(db: Session, gym_id: int):
#     return (
#       db.query(
#         models.Customer.name,
#         models.Customer.email,
#         models.Customer.phone,
#         models.Package.name.label("membership"),
#         models.Customer.gender
#       )
#       .join(models.Package, models.Customer.package_id == models.Package.package_id, isouter=True)
#       .filter(models.Customer.gym_id == gym_id)
#       .all()
#     )
def get_customers_for_gym(db: Session, gym_id: int):
    return (
        db.query(models.Customer)
          .options(joinedload(models.Customer.package))
          .filter(models.Customer.gym_id == gym_id)
          .all()
    )

def get_average_clv(db: Session, gym_id: int) -> Decimal | float:
    """
    Calculate the average CLV for all customers of a specific gym.

    :param db: Database session
    :param gym_id: ID of the gym to filter customers
    :return: The average CLV value
    """
    avg_raw = (
        db.query(func.avg(models.CLV.clv_value))
          .join(models.Customer)
          .filter(models.Customer.gym_id == gym_id)
          .scalar()
    )
    # If no records, treat as zero
    if avg_raw is None:
        return Decimal("0.00")

    # Ensure it’s a Decimal
    avg_dec = avg_raw if isinstance(avg_raw, Decimal) else Decimal(str(avg_raw))

    # Quantize to exactly two places, rounding half-up
    return avg_dec.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)



    #
    #
    # # Query the CLV values for all customers related to the gym
    # clv_values = db.query(models.CLV.clv_value).join(models.Customer).filter(models.Customer.gym_id == gym_id).all()
    #
    # # If there are no CLV records, return 0 as the average
    # if not clv_values:
    #     return Decimal(0)
    #
    # # Calculate the sum of CLV values and the count of CLV entries
    # total_clv = sum([clv.clv_value for clv in clv_values])
    # average_clv = total_clv / len(clv_values)
    #
    # return average_clv


def get_customers_by_package(db: Session, gym_id: int):
    """
    Returns a list of (package_name, total_customers) tuples
    for all packages (including those with zero customers)
    belonging to the given gym.
    """
    return (
        db.query(
            models.Package.name.label("package_name"),
            func.count(models.Customer.customer_id).label("total_customers"),
        )
        .outerjoin(
            models.Customer,
            models.Customer.package_id == models.Package.package_id
        )
        .filter(
            models.Package.gym_id == gym_id
        )
        .group_by(
            models.Package.package_id,
            models.Package.name
        )
        .order_by(
            models.Package.name
        )
        .all()
    )

def get_risk_customers_for_gym(db: Session, gym_id: int):
    """
    Returns customers marked as 'At Risk' along with their last visit date, membership package,
    and inactive days based on the difference from the last visit.
    """
    # Querying risk customers (those with the "At Risk" customer segment in the RFM table)
    risk_customers = db.query(
        models.Customer.name,
        models.Attendance.check_out.label('last_visit'),
        models.Customer.package_id,
        func.datediff(func.current_date(), models.Attendance.check_out).label('inactive_days')
    ).join(
        models.RFM, models.RFM.customer_id == models.Customer.customer_id
    ).join(
        models.Attendance, models.Attendance.customer_id == models.Customer.customer_id
    ).filter(
        models.RFM.customer_segment == 'At Risk',
        models.Customer.gym_id == gym_id
    ).order_by(models.Attendance.check_out.desc()).all()

    # Mapping to desired format (including the 'membership' package info)
    risk_customer_data = []
    for customer in risk_customers:
        # Assuming you want to return the package's name (could be modified based on the 'Package' table structure)
        membership_name = "N/A"  # Default value if package_id is None
        if customer.package_id:
            membership_name = "Package ID: " + str(customer.package_id)  # Replace with actual package name if needed
        risk_customer_data.append({
            "name": customer.name,
            "last_visit": customer.last_visit,
            "membership": membership_name,
            "inactive_days": customer.inactive_days
        })

    return risk_customer_data


def get_risk_customer_count_for_gym(db: Session, gym_id: int) -> int:
    """
    Returns the count of 'At Risk' customers for a specific gym.
    """
    count = db.query(models.Customer.customer_id).join(
        models.RFM, models.RFM.customer_id == models.Customer.customer_id
    ).filter(
        models.RFM.customer_segment == 'At Risk',
        models.Customer.gym_id == gym_id
    ).count()

    return count




def count_recent_customers(
    db: Session,
    gym_id: int,
    recency_threshold: int = 7
) -> int:
    """
    Return the number of customers belonging to `gym_id`
    whose RFM.recency_score is less than recency_threshold.
    """
    return (
        db.query(func.count(models.RFM.rfm_id))
          .join(models.Customer, models.Customer.customer_id == models.RFM.customer_id)
          .filter(
              models.Customer.gym_id == gym_id,
              models.RFM.recency_score < recency_threshold
          )
          .scalar()
    )