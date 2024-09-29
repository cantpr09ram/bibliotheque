from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.auth import routers
from app.services.main import api_router
from app.database import init_db

load_dotenv()

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize database connection
init_db()

# Include routers
app.include_router(routers.router)
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}