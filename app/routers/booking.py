from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=list[schemas.Seat])
def book_seats(request: schemas.BookingRequest, db: Session = Depends(get_db)):
    show = db.query(models.Show).filter(models.Show.id == request.show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    
    booked_seats = []
    for seat_req in request.seats:
        seat = db.query(models.Seat).filter(
            models.Seat.row == seat_req.row,
            models.Seat.col == seat_req.col,
            models.Seat.show_id == request.show_id
        ).first()
        if not seat or seat.booked:
            raise HTTPException(status_code=400, detail="Seat not available")
        seat.booked = True
        db.add(seat)
        booked_seats.append(seat)
    
    db.commit()
    return booked_seats
