from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import models, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/movie/{movie_id}")
def movie_analytics(
    movie_id: int,
    start_date: str = Query(None, description="Start date in YYYY-MM-DD"),
    end_date: str = Query(None, description="End date in YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    # Validate movie exists
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Query shows for this movie
    shows_query = db.query(models.Show).filter(models.Show.movie_id == movie_id)
    
    if start_date:
        shows_query = shows_query.filter(models.Show.start_time >= start_date)
    if end_date:
        shows_query = shows_query.filter(models.Show.start_time <= end_date)
    
    shows = shows_query.all()
    
    # Count tickets booked and calculate GMV
    total_tickets = 0
    for show in shows:
        booked_seats = db.query(models.Seat).filter(
            models.Seat.show_id == show.id,
            models.Seat.booked == True
        ).count()
        total_tickets += booked_seats
    
    gmv = total_tickets * movie.price
    
    return {
        "movie_id": movie.id,
        "title": movie.title,
        "total_tickets_booked": total_tickets,
        "gmv": gmv
    }
