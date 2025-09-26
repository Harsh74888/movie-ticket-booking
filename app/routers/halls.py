from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get all halls
@router.get("/", response_model=list[schemas.Hall])
def get_halls(db: Session = Depends(get_db)):
    return db.query(models.Hall).all()


# Create a hall
@router.post("/", response_model=schemas.Hall)
def create_hall(hall: schemas.HallCreate, db: Session = Depends(get_db)):
    db_hall = models.Hall(**hall.dict())
    db.add(db_hall)
    db.commit()
    db.refresh(db_hall)
    return db_hall


# Get hall by ID
@router.get("/{hall_id}", response_model=schemas.Hall)
def get_hall(hall_id: int, db: Session = Depends(get_db)):
    return db.query(models.Hall).filter(models.Hall.id == hall_id).first()


# Update hall
@router.put("/{hall_id}", response_model=schemas.Hall)
def update_hall(hall_id: int, hall: schemas.HallCreate, db: Session = Depends(get_db)):
    db_hall = db.query(models.Hall).filter(models.Hall.id == hall_id).first()
    if db_hall:
        for key, value in hall.dict().items():
            setattr(db_hall, key, value)
        db.commit()
        db.refresh(db_hall)
    return db_hall


# Delete hall
@router.delete("/{hall_id}")
def delete_hall(hall_id: int, db: Session = Depends(get_db)):
    db_hall = db.query(models.Hall).filter(models.Hall.id == hall_id).first()
    if db_hall:
        db.delete(db_hall)
        db.commit()
        return {"message": "Hall deleted successfully"}
    return {"message": "Hall not found"}
