from fastapi import FastAPI
import models
from database import engine
from routers import post, user, auth
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",  # Allow all origins (for development)
    "http://localhost:3000", # Allow localhost:3000, where react app is running.
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)