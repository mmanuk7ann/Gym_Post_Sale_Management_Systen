# 🤖 Modeling Service

The `ds` service is responsible for performing core customer analytics, including **RFM segmentation** and **Customer Lifetime Value (CLV)** estimation. It uses synthetic transactional and attendance data to generate retention insights, which are saved to the PostgreSQL database for further visualization or analysis.

---

## 🧱 Architecture Overview

This pipeline is implemented using:

- **pandas** – Data manipulation
- **SQLAlchemy** – PostgreSQL interaction
- **scikit-learn** – KMeans clustering
- **matplotlib** – (Optional) plotting support
- **dotenv** – Credential management
- **Python + Docker** – Containerized execution of model logic

---

## 📦 Input & Output Flow

### 🔽 Input:
- Automatically generated CSVs in `etl/data/`:
  - `attendance.csv`
  - `transactions.csv`
  - `customers.csv`
  - `packages.csv`

### ⬆ Output:
- DataFrames saved as tables:
  - `rfm` – Recency, Frequency, Monetary segmentation
  - `clv` – Estimated customer value and behavior type

---

## 🔍 Model Components

### 1. **RFM Segmentation**

- **Recency**: Days since last attendance
- **Frequency**: Count of attendance records
- **Monetary**: Sum of transaction amounts
- Data is scaled using `StandardScaler`, then clustered using `KMeans` (`n_clusters=4`).
- Segments are mapped to:
  - `Loyalist`
  - `At Risk`
  - `New/Potential`
  - `High-Value`

```python
kmeans = KMeans(n_clusters=4, random_state=42)
rfm['Segment'] = kmeans.fit_predict(rfm_scaled)
```

---

### 2. **CLV Estimation**

- **AOV (Average Order Value)** = Total spend / Number of orders
- **CLV** = AOV × Frequency × 1 (fixed lifespan for simplicity)

Output columns include:
- `clv_value`
- `average_order_value`
- `predicted_customer_type`

---

### 3. **Retention Rate Calculation**

Customers with recency > 90 days are considered churned.  
Retention is calculated as:

```python
retention_rate = (1 - churned / total) * 100
```

Printed in console after model run.

---

## 💾 Output Tables in Database

| Table | Description |
|-------|-------------|
| `rfm` | Contains RFM scores and cluster-based segments |
| `clv` | Contains CLV values and predicted customer type |

---

## 📂 File Structure

| File               | Purpose                              |
|--------------------|--------------------------------------|
| `ds_model.py`      | Main script: loads data, runs models |
| `.env`             | Contains `DATABASE_URL` and secrets  |
| `etl/data/*.csv`   | Synthetic input datasets             |
| `Dockerfile`       | Container setup for reproducibility  |

---

## 🐳 Execution

The modeling pipeline is triggered by running:

```bash
python ds_model.py
```

This script:
1. Loads `.csv` files
2. Computes RFM + CLV
3. Calculates retention rate
4. Pushes results to PostgreSQL

Make sure `.env` is configured correctly and the PostgreSQL container is running.

---

## 🔧 Environment Setup

Dependencies (`ds/requirements.txt`):

```text
pandas
sqlalchemy
psycopg2-binary
python-dotenv
scikit-learn
matplotlib
```

Install with:

```bash
pip install -r ds/requirements.txt
```