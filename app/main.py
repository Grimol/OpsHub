from fastapi import FastAPI

from app.api.v1 import audit_logs, projects, tickets, users


def create_app() -> FastAPI:
    app = FastAPI(title="OpsHub", version="1.0.0")
    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(projects.router, prefix="/projects", tags=["projects"])
    app.include_router(tickets.router, prefix="/api/v1/tickets", tags=["tickets"])
    app.include_router(audit_logs.router, prefix="/api/v1/audit-logs", tags=["audit-logs"])
    return app


app = create_app()
