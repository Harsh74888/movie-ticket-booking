from sqlalchemy.orm import Session
from . import models, schemas

def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def create_theater(db: Session, theater: schemas.TheaterCreate):
    db_theater = models.Theater(**theater.dict())
    db.add(db_theater)
    db.commit()
    db.refresh(db_theater)
    return db_theater

def create_hall(db: Session, hall: schemas.HallCreate):
    db_hall = models.Hall(**hall.dict())
    db.add(db_hall)
    db.commit()
    db.refresh(db_hall)
    return db_hall

def create_show(db: Session, show: schemas.ShowCreate):
    db_show = models.Show(**show.dict())
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return db_show

def book_seats(db: Session, show_id: int, seats: list):
    booked = []
    for seat in seats:
        db_seat = db.query(models.Seat).filter_by(show_id=show_id, row=seat.row, col=seat.col).first()
        if db_seat and db_seat.booked:
            raise Exception(f"Seat {seat.row}-{seat.col} already booked!")
        elif db_seat:
            db_seat.booked = True
            booked.append(db_seat)
        else:
            new_seat = models.Seat(row=seat.row, col=seat.col, booked=True, show_id=show_id)
            db.add(new_seat)
            booked.append(new_seat)
    db.commit()
    return booked
