from pydantic import BaseModel

class PodAssign(BaseModel):
    employee_id: int
    pod_id: int

class PodRecommend(BaseModel):
    recommended_user_id: int