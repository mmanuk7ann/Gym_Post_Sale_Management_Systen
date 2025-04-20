from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from Database import models
from Database.schema import *

from Database.database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gym Management API")

# --- Gym Endpoints ---

@app.post("/gyms/", response_model=GymOut, status_code=201)
def create_gym(gym: GymCreate, db: Session = Depends(get_db)):
    db_gym = models.Gym(**gym.dict())
    db.add(db_gym); db.commit(); db.refresh(db_gym)
    return db_gym

@app.get("/gyms/", response_model=list[GymOut])
def read_gyms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Gym).offset(skip).limit(limit).all()

@app.get("/gyms/{gym_id}", response_model=GymOut)
def read_gym(gym_id: int, db: Session = Depends(get_db)):
    gym = db.query(models.Gym).get(gym_id)
    if not gym:
        raise HTTPException(404, "Gym not found")
    return gym

@app.put("/gyms/{gym_id}", response_model=GymOut)
def update_gym(gym_id: int, data: GymUpdate, db: Session = Depends(get_db)):
    gym = db.query(models.Gym).get(gym_id)
    if not gym:
        raise HTTPException(404, "Gym not found")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(gym, k, v)
    db.commit(); db.refresh(gym)
    return gym

@app.delete("/gyms/{gym_id}", status_code=204)
def delete_gym(gym_id: int, db: Session = Depends(get_db)):
    gym = db.query(models.Gym).get(gym_id)
    if not gym:
        raise HTTPException(404, "Gym not found")
    db.delete(gym); db.commit()


# --- Package Endpoints ---

@app.post("/packages/", response_model=PackageOut, status_code=201)
def create_package(pkg: PackageCreate, db: Session = Depends(get_db)):
    db_pkg = models.Package(**pkg.dict())
    db.add(db_pkg); db.commit(); db.refresh(db_pkg)
    return db_pkg

@app.get("/packages/", response_model=list[PackageOut])
def read_packages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Package).offset(skip).limit(limit).all()

@app.get("/packages/{package_id}", response_model=PackageOut)
def read_package(package_id: int, db: Session = Depends(get_db)):
    pkg = db.query(models.Package).get(package_id)
    if not pkg:
        raise HTTPException(404, "Package not found")
    return pkg

@app.put("/packages/{package_id}", response_model=PackageOut)
def update_package(package_id: int, data: PackageUpdate, db: Session = Depends(get_db)):
    pkg = db.query(models.Package).get(package_id)
    if not pkg:
        raise HTTPException(404, "Package not found")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(pkg, k, v)
    db.commit(); db.refresh(pkg)
    return pkg

@app.delete("/packages/{package_id}", status_code=204)
def delete_package(package_id: int, db: Session = Depends(get_db)):
    pkg = db.query(models.Package).get(package_id)
    if not pkg:
        raise HTTPException(404, "Package not found")
    db.delete(pkg); db.commit()
