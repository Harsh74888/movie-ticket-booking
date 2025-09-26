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


# Get all theaters
@router.get("/", response_model=list[schemas.Theater])
def get_theaters(db: Session = Depends(get_db)):
    return db.query(models.Theater).all()


# Create a theater
@router.post("/", response_model=schemas.Theater)
def create_theater(theater: schemas.TheaterCreate, db: Session = Depends(get_db)):
    db_theater = models.Theater(**theater.dict())
    db.add(db_theater)
    db.commit()
    db.refresh(db_theater)
    return db_theater


# Get theater by ID
@router.get("/{theater_id}", response_model=schemas.Theater)
def get_theater(theater_id: int, db: Session = Depends(get_db)):
    return db.query(models.Theater).filter(models.Theater.id == theater_id).first()


# Update theater
@router.put("/{theater_id}", response_model=schemas.Theater)
def update_theater(theater_id: int, theater: schemas.TheaterCreate, db: Session = Depends(get_db)):
    db_theater = db.query(models.Theater).filter(models.Theater.id == theater_id).first()
    if db_theater:
        for key, value in theater.dict().items():
            setattr(db_theater, key, value)
        db.commit()
        db.refresh(db_theater)
    return db_theater


# Delete theater
@router.delete("/{theater_id}")
def delete_theater(theater_id: int, db: Session = Depends(get_db)):
    db_theater = db.query(models.Theater).filter(models.Theater.id == theater_id).first()
    if db_theater:
        db.delete(db_theater)
        db.commit()
        return {"message": "Theater deleted successfully"}
    return {"message": "Theater not found"}
