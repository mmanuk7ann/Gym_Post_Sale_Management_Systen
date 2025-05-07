from fastapi import FastAPI
from Database.database import engine, Base
from routers import auth, gyms, customers, email


# Create all tables (in prod use Alembic instead)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gym Management API")

app.include_router(auth.router)
app.include_router(gyms.router)
app.include_router(customers.router)
app.include_router(email.router)


@app.get("/health")
def health():
    return True