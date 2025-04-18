from fastapi import FastAPI
from app.api import routes

app = FastAPI()

app.include_router(routes.dashboard_router)
app.include_router(routes.lms_router)
app.include_router(routes.pods_router)
app.include_router(routes.auth_router)