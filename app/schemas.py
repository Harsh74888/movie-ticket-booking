from pydantic import BaseModel
from typing import List
import datetime

class MovieBase(BaseModel):
    title: str
    description: str
    duration: int
    price: float

class MovieCreate(MovieBase): 
    pass

class Movie(MovieBase):
    id: int
    class Config:
        from_attributes = True   # updated

class TheaterBase(BaseModel):
    name: str
    location: str

class TheaterCreate(TheaterBase): 
    pass

class Theater(TheaterBase):
    id: int
    class Config:
        from_attributes = True   # updated

class HallBase(BaseModel):
    name: str
    rows: int
    seats_per_row: int

class HallCreate(HallBase):
    theater_id: int

class Hall(HallBase):
    id: int
    class Config:
        from_attributes = True   # updated

class ShowBase(BaseModel):
    movie_id: int
    hall_id: int
    start_time: datetime.datetime

class ShowCreate(ShowBase): 
    pass

class Show(ShowBase):
    id: int
    class Config:
        from_attributes = True   # updated

class SeatBase(BaseModel):
    row: int
    col: int

class Seat(SeatBase):
    id: int
    booked: bool
    class Config:
        from_attributes = True   # updated

class BookingRequest(BaseModel):
    show_id: int
    seats: List[SeatBase]
