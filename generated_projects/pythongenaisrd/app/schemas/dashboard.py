from pydantic import BaseModel

class DashboardTile(BaseModel):
    title: str
    value: str