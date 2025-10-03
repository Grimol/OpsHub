from fastapi import FastAPI
from app.api.v1 import users, projects

def create_app() -> FastAPI:
    app = FastAPI(title="OpsHub", version="1.0.0")
    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(projects.router, prefix="/projects", tags=["projects"])
    return app

app = create_app()