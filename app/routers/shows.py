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


# Get all shows
@router.get("/", response_model=list[schemas.Show])
def get_shows(db: Session = Depends(get_db)):
    return db.query(models.Show).all()


# Create a show
@router.post("/", response_model=schemas.Show)
def create_show(show: schemas.ShowCreate, db: Session = Depends(get_db)):
    db_show = models.Show(**show.dict())
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return db_show


# Get show by ID
@router.get("/{show_id}", response_model=schemas.Show)
def get_show(show_id: int, db: Session = Depends(get_db)):
    return db.query(models.Show).filter(models.Show.id == show_id).first()


# Update show
@router.put("/{show_id}", response_model=schemas.Show)
def update_show(show_id: int, show: schemas.ShowCreate, db: Session = Depends(get_db)):
    db_show = db.query(models.Show).filter(models.Show.id == show_id).first()
    if db_show:
        for key, value in show.dict().items():
            setattr(db_show, key, value)
        db.commit()
        db.refresh(db_show)
    return db_show


# Delete show
@router.delete("/{show_id}")
def delete_show(show_id: int, db: Session = Depends(get_db)):
    db_show = db.query(models.Show).filter(models.Show.id == show_id).first()
    if db_show:
        db.delete(db_show)
        db.commit()
        return {"message": "Show deleted successfully"}
    return {"message": "Show not found"}
