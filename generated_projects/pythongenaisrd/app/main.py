from fastapi import FastAPI
from app.api.routes import dashboard_router, lms_router, pods_router, auth_router

app = FastAPI()

app.include_router(dashboard_router, prefix="/api/dashboard")
app.include_router(lms_router, prefix="/api/lms")
app.include_router(pods_router, prefix="/api/pods")
app.include_router(auth_router, prefix="/api/auth")