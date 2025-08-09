from fastapi import FastAPI
from app.routers import auth, users, projects

app = FastAPI(
    title="Mahi Crowdfunding API",
    description="API for a crowdfunding platform",
    version="0.1.0"
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Mahi Crowdfunding API"}
