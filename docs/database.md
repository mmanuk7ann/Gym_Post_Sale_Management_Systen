# 🗃️ Database Documentation

This service manages the **PostgreSQL database** for the gym management system. It stores all backend data related to gyms, members, packages, attendance, transactions, and analytics (RFM & CLV). The database is automatically populated with synthetic data each time the system is initialized, making it ideal for testing and demonstration purposes.

---

## 🧩 ER Diagram

The schema includes the following interconnected tables:

- `gyms`
- `customers`
- `packages`
- `attendance`
- `transactions`
- `rfm`
- `clv`

📎 See schema image: 
![ERD](docs/ERD.jpg)

---

## 📊 Table Descriptions

### 🏢 `gyms`

Stores registered gyms and login credentials.

| Column         | Type     | Description          |
|----------------|----------|----------------------|
| `gym_id`       | int      | Primary key          |
| `name`         | varchar  | Gym name             |
| `username`     | varchar  | Login username       |
| `email`        | varchar  | Login email          |
| `hashed_password` | varchar | Encrypted password |
| `address`      | varchar  | Address              |
| `phone`        | varchar  | Contact number       |

---

### 👥 `customers`

Contains all gym members.

| Column         | Type     | Description               |
|----------------|----------|---------------------------|
| `customer_id`  | int      | Primary key               |
| `gym_id`       | int      | Foreign key → gyms        |
| `name`         | varchar  | Full name                 |
| `email`        | varchar  | Email                     |
| `phone`        | varchar  | Phone number              |
| `birth_date`   | date     | Birth date                |
| `gender`       | varchar  | Gender                    |
| `join_date`    | date     | Membership start date     |
| `status`       | varchar  | Active, frozen, cancelled |
| `package_id`   | int      | Foreign key → packages    |
| `trainer_id`   | int      | Optional trainer link     |

---

### 📦 `packages`

Membership options defined by each gym.

| Column         | Type     | Description              |
|----------------|----------|--------------------------|
| `package_id`   | int      | Primary key              |
| `gym_id`       | int      | Foreign key → gyms       |
| `name`         | varchar  | Plan name                |
| `duration_months` | int   | Duration in months       |
| `price`        | decimal  | Price of the package     |
| `description`  | text     | Extra details            |

---

### 🕒 `attendance`

Tracks customer check-in and check-out activity.

| Column         | Type     | Description               |
|----------------|----------|---------------------------|
| `attendance_id`| int      | Primary key               |
| `customer_id`  | int      | Foreign key → customers   |
| `check_in`     | datetime | Entry time                |
| `check_out`    | datetime | Exit time                 |

---

### 💸 `transactions`

Financial transactions linked to each customer.

| Column         | Type     | Description               |
|----------------|----------|---------------------------|
| `transaction_id` | int    | Primary key               |
| `customer_id`    | int    | Foreign key → customers   |
| `amount`         | int    | Payment amount            |
| `date`           | date   | Payment date              |

---

### 📈 `rfm`

Recency-Frequency-Monetary scores for segmentation.

| Column           | Type     | Description               |
|------------------|----------|---------------------------|
| `rfm_id`         | int      | Primary key               |
| `customer_id`    | int      | Foreign key → customers   |
| `recency_score`  | int      | Days since last activity  |
| `frequency_score`| int      | Visit frequency           |
| `monetary_score` | decimal  | Total amount spent        |
| `customer_segment` | varchar| Segment classification    |

---

### 💡 `clv`

Predicted Customer Lifetime Value metrics.

| Column                 | Type     | Description                    |
|------------------------|----------|--------------------------------|
| `clv_id`               | int      | Primary key                    |
| `customer_id`          | int      | Foreign key → customers        |
| `clv_value`            | decimal  | Estimated lifetime value       |
| `average_order_value`  | decimal  | Avg. purchase amount           |
| `predicted_customer_type` | varchar | Predicted behavior segment |

---

## 🧪 Data Generation

This project uses **synthetic data**, automatically generated at runtime for testing purposes. All tables are filled with realistic but fake data (e.g. names, emails, payment history) to enable functional testing of API endpoints, dashboards, and analytics.

- No CSVs or external files are used to load the data.
- Each time the app is restarted, a fresh dataset is generated.
- Useful for showcasing features like churn detection and lifetime value predictions.

---

## 🛠️ Dependencies

- `SQLAlchemy` — ORM for defining models and managing schema
- `psycopg2-binary` — PostgreSQL driver
- `pandas` — Used optionally for tabular manipulation (e.g. RFM/CLV scoring)
- `dotenv` — Environment variable loading

---

## 🔐 Configuration

All credentials are stored in a `.env` file in the root of the project:

```env
DATABASE_URL=postgresql+psycopg2://postgres:password@db:5432/demodb
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=demodb
PGADMIN_EMAIL=admin@admin.com 
PGADMIN_PASSWORD=admin
SECRET_KEY=secret-key
