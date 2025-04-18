def test_apply_leave(client):
    data = {"start_date": "2022-01-01", "end_date": "2022-01-05", "reason": "Vacation"}
    response = client.post("/api/lms/leaves/apply", json=data)
    assert response.status_code == 201
    assert response.json()["message"] == "Leave applied successfully"

def test_assign_employee_to_pod(client):
    data = {"employee_id": 1, "pod_id": 1}
    response = client.post("/api/pods/assign", json=data)
    assert response.status_code == 201
    assert response.json()["message"] == "Employee assigned to pod successfully"

def test_recommend_employee_for_pod(client):
    pod_id = 1
    data = {"recommended_user_id": 2}
    response = client.post(f"/api/pods/{pod_id}/recommend", json=data)
    assert response.status_code == 201
    assert response.json()["message"] == "Employee recommended for pod successfully"