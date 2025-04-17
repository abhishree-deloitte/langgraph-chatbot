from pydantic import BaseModel

class PodAssignment(BaseModel):
    user_id: int

class PodDetails(BaseModel):
    id: int
    name: str

class PodRecommendation(BaseModel):
    recommended_user_id: int