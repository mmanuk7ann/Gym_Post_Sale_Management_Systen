# 📘 API Endpoints Documentation

This document describes key API endpoints for the MVP version of the application.

---

## 📧 POST `/email/send` — Send Email to Customer

**Description:**  
Sends an email to a specified customer on behalf of the authenticated gym. The email is sent asynchronously as a background task, so the request returns immediately.

**Authentication:** Internal — gym must be authenticated

**Request Body (JSON):**
```json
{
  "email": "customer@example.com",
  "text": "Your subscription has been updated."
}
```

---

## 👥 GET `/customers/customer/all` — List All Customers

**Description:**  
Retrieves a list of all customers associated with the currently authenticated gym.

**Authentication:** Gym must be logged in (JWT token)

**Response:**
```json
[
  {
    "customer_id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "join_date": "2024-12-01",
    "status": "active"
  }
]
```

---

## ⚠️ GET `/customers/customer/risk` — List At-Risk Customers

**Description:**  
Returns a list of customers flagged as "at risk" of churning, based on internal logic such as infrequent attendance, nearing the end of subscription, or lack of engagement.

**Authentication:** Gym must be logged in (JWT token)

**Response:**
```json
[
  {
    "customer_id": 7,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "risk_status": "high",
    "last_attendance": "2025-04-01"
  }
]
```

---

## 📊 GET `/gyms/gym/members-count` — Get Total Member Count

**Description:**  
Returns the total number of registered members (customers) currently associated with the authenticated gym. Useful for dashboards and analytics.

**Authentication:** Gym must be logged in (JWT token)

**Response:**
```json
{
  "count": 42
}
```

---

## 📈 GET `/gyms/gym/average-clv` — Get Average Customer Lifetime Value (CLV)

**Description:**  
Returns the average Customer Lifetime Value (CLV) for all customers registered under the authenticated gym. Useful for understanding long-term customer value and guiding retention strategies.

**Authentication:** Gym must be logged in (JWT token)

**Response:**
```json
{
  "average_clv": 2485.75
}
```

---

## 📦 GET `/gyms/gym/customers-by-package` — Customers Grouped by Package

**Description:**  
Returns the total number of customers grouped by the subscription package they are enrolled in, specific to the authenticated gym. Useful for visualizing package popularity and usage distribution.

**Authentication:** Gym must be logged in (JWT token)

**Response:**
```json
{
  "packages": [
    {
      "package_name": "Plus Plan",
      "total_customers": 18
    },
    {
      "package_name": "Basic Plan",
      "total_customers": 32
    }
  ]
}
```

---

## 🧮 GET `/gyms/gym/risk-count` — Count Risk Customers

**Description:**  
Returns the total number of at-risk customers under the authenticated gym.

**Authentication:** Gym must be logged in (JWT token)

**Response:**
```json
{
  "risk_count": 8
}
```

---

## 📅 GET `/gyms/gym/last_week_visits` — Last Week Visits

**Description:**  
Returns the number of visits made by each customer in the last 7 days.

**Authentication:** Gym must be logged in (JWT token)

**Response:**
```json
[
  {
    "customer_id": 5,
    "name": "Alex Johnson",
    "visits": 3
  },
  {
    "customer_id": 9,
    "name": "Maria Lopez",
    "visits": 1
  }
]
```

---

# 🔧 System

## 🩺 GET `/health` — Health Check

**Description:**  
Returns a simple status to indicate that the backend is running.

**Authentication:** Public

**Response:**
```json
{
  "status": "ok"
}
```