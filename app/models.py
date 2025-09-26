from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

# ----------------------
# Movie
# ----------------------
class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # in minutes
    price = Column(Float, nullable=False)
    
    shows = relationship("Show", back_populates="movie")


# ----------------------
# Theater
# ----------------------
class Theater(Base):
    __tablename__ = "theaters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    
    halls = relationship("Hall", back_populates="theater")


# ----------------------
# Hall
# ----------------------
class Hall(Base):
    __tablename__ = "halls"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rows = Column(Integer, nullable=False)
    seats_per_row = Column(Integer, nullable=False)
    theater_id = Column(Integer, ForeignKey("theaters.id"), nullable=False)
    
    theater = relationship("Theater", back_populates="halls")
    shows = relationship("Show", back_populates="hall")


# ----------------------
# Show
# ----------------------
class Show(Base):
    __tablename__ = "shows"
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    hall_id = Column(Integer, ForeignKey("halls.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    
    movie = relationship("Movie", back_populates="shows")
    hall = relationship("Hall", back_populates="shows")
    seats = relationship("Seat", back_populates="show")


# ----------------------
# Seat
# ----------------------
class Seat(Base):
    __tablename__ = "seats"
    
    id = Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    row = Column(Integer, nullable=False)
    col = Column(Integer, nullable=False)
    booked = Column(Boolean, default=False)
    
    show = relationship("Show", back_populates="seats")


