from fastapi import APIRouter, Depends
from app.services.pods import get_pod_details, recommend_employee
from app.schemas.pods import PodDetails, RecommendEmployee
from app.dependencies import get_db_session

router = APIRouter()

@router.get("/{pod_id}/details")
async def get_pod_details(pod_id: int, db_session=Depends(get_db_session)):
    return get_pod_details(pod_id, db_session)

@router.post("/{pod_id}/recommend")
async def recommend_employee_for_pod(pod_id: int, employee: RecommendEmployee, db_session=Depends(get_db_session)):
    return recommend_employee(pod_id, employee, db_session)