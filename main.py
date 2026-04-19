from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as trip_router

app = FastAPI(title="AI Travel Agent API", version="1.0.0")

# Add CORS middleware
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(trip_router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "AI Travel Agent Backend is running."}

@app.get("/health")
def health():
    return {"status": "ok"}

# To run: uvicorn main:app --reload
