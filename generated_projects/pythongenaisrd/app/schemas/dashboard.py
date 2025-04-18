from pydantic import BaseModel

class DashboardTileSchema(BaseModel):
    id: int
    name: str