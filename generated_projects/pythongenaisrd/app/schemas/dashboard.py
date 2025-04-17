from pydantic import BaseModel

class DashboardTile(BaseModel):
    id: int
    title: str
    description: str