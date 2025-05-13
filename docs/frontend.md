# 🖥️ Frontend Interface

The frontend is a dynamic, interactive dashboard built with **Streamlit**, designed to provide gym managers with real-time insights and actionable tools. It consumes RESTful API endpoints exposed by the backend and visualizes metrics like member counts, risk assessments, and customer segmentation.

---

## ⚙️ Tech Stack

- **Streamlit** — Main frontend framework
- **Python** — Logic and layout
- **Requests** — REST API communication
- **Pandas** — Table and chart formatting
- **Docker** — Containerized deployment (`Dockerfile` provided)

---

## 🧭 Navigation

The sidebar contains three main tabs:

- **Dashboard**: Visual KPIs and a bar chart of membership distribution
- **Customers**: Searchable and filterable member list
- **Risk Management**: At-risk members with email outreach

---

## 📊 Dashboard Tab

Displays four key metrics:
- Total Members
- At-Risk Members
- Average CLV
- Last Week Visits

It also shows a **bar chart** of customers by package using real-time data from the `/customers-by-package` endpoint.

---

## 👥 Customers Tab

This view displays a searchable and filterable list of all registered customers:
- Filters: Gender, Membership Type, Name
- Data is fetched from: `GET /customers/customer/all`

---

## ⚠️ Risk Management Tab

Identifies at-risk members and lets admins take action:
- Displays last visit, membership type, and inactivity days
- Admin can **send custom emails** via `POST /email/send`
- Filters: Membership Type, Name

---

## 🔌 API Integration

All data is fetched live from the backend using `requests.get()`:
- `/gyms/gym/members-count`
- `/gyms/gym/average-clv`
- `/gyms/gym/risk-count`
- `/gyms/gym/last_week_visits`
- `/customers/customer/all`
- `/customers/customer/risk`
- `/gyms/gym/customers-by-package`
- `/email/send`

---

## 🐳 Dockerized Setup

The frontend runs inside a Docker container on port `8501`.

**Dockerfile:**
```dockerfile
FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev libfreetype6-dev libpng-dev libjpeg-dev \
    libblas-dev liblapack-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true", "--server.runOnSave=true"]
```

---

## 📂 Folder Structure

```
frontend/
├── app.py              # Main dashboard logic
├── Dockerfile          # Container config
├── requirements.txt    # Python dependencies
```

---

## 🧪 Notes

- Data is regenerated on each run using synthetic logic
- The dashboard is **self-refreshing** based on API calls
- All business logic is handled by the backend; frontend is display + interaction layer only

---

## 🚀 How to Run

```bash
cd frontend
docker build -t gym-dashboard .
docker run -p 8501:8501 gym-dashboard
```

Visit [http://localhost:8501](http://localhost:8501) in your browser to interact with the dashboard.