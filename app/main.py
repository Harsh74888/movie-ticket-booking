from fastapi import FastAPI
from app.database import Base, engine
from app.routers import movies, theaters, halls, shows, booking, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Booking API")

# Include Routers with prefixes
app.include_router(movies.router, prefix="/movies", tags=["Movies"])
app.include_router(theaters.router, prefix="/theaters", tags=["Theaters"])
app.include_router(halls.router, prefix="/halls", tags=["Halls"])
app.include_router(shows.router, prefix="/shows", tags=["Shows"])
app.include_router(booking.router, prefix="/bookings", tags=["Bookings"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
