from pydantic import BaseModel

class AssignPodSchema(BaseModel):
    employee_id: int
    pod_id: int

class RecommendPodSchema(BaseModel):
    employee_ids: List[int]