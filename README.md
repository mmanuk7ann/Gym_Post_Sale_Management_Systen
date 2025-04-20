## **Project Focus:** Customer Retention & CLV Optimization for Gyms

--- 

## **Authors**

- Project/Product Manager - Artsvik Avetisyan
- Database Developer - Levon Titanyan
- Back-end Developer - Armen Ghazaryan
- Frond-end Developer - Ani Gharibyan
- Data Analyst/Scientist - Manuk Manukyan

---

The problem area lies in **Customer Retention** and **Customer Lifetime Value optimization** in the fitness industry.

Many gyms lack proactive systems to detect disengaged members and intervene before they churn.  
Extended periods of absence not only signal a higher risk of churn but can also lead to **customer demotivation**, decreased engagement, and weakened **brand loyalty**.  

---

## Installation

Ensure you have the following prerequisites installed:

1. Clone the repository:

```bash
git clone https://github.com/DS-223/Group-3.git
cd Group-3
```

2. Build and start the Docker containers:

```bash
docker-compose up --build
```

## Project Structure

```bash
PythonPackageProject/ # GitHub repo root ├── yourapplications/ # Contains all services │ ├── docker-compose.yaml # Docker Compose file │ ├── .env # Environment variables │ ├── service1/ # postgres │ │ ├── *.py │ │ └── Dockerfile │ ├── service2/ # pgadmin │ │ ├── *.py │ │ └── Dockerfile │ ├── service3/ # ETL-related │ │ ├── *.py │ │ └── requirements.txt │ └── Dockerfile # If needed ├── example.ipynb # Demo notebook ├── docs/ # Documentation │ └── ... ├── .gitignore ├── requirements_docs.txt # Doc requirements ├── README.md └── LICENSE
```

## ER Diagram

![ER Diagram](docs/ERD.png)
