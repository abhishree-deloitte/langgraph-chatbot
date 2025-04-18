from pydantic import BaseModel

class PodDetails(BaseModel):
    # define pod details schema
    pass

class RecommendEmployee(BaseModel):
    recommended_user_id: int