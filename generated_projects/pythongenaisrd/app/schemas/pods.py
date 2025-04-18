from pydantic import BaseModel

class PodAssignment(BaseModel):
    employee_id: int
    pod_id: int

class PodRecommendation(BaseModel):
    recommended_user_id: int