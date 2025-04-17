def test_dashboard_tiles(client):
    response = client.get("/api/dashboard/tiles")
    assert response.status_code == 200

def test_apply_leave(client):
    data = {"start_date": "2022-01-01", "end_date": "2022-01-02", "reason": "Test reason"}
    response = client.post("/api/lms/leaves/apply", json=data)
    assert response.status_code == 201

def test_retrieve_leave_status(client):
    response = client.get("/api/lms/leaves/status")
    assert response.status_code == 200

def test_approve_leave(client):
    data = {"status": "approved"}
    response = client.patch("/api/lms/leaves/1/approve", json=data)
    assert response.status_code == 200

def test_assign_employee_to_pod(client):
    data = {"employee_id": 1, "pod_id": 1}
    response = client.post("/api/pods/assign", json=data)
    assert response.status_code == 201

def test_get_pod_details(client):
    response = client.get("/api/pods/1/details")
    assert response.status_code == 200

def test_recommend_employee_for_pod(client):
    data = {"recommended_user_id": 2}
    response = client.post("/api/pods/1/recommend", json=data)
    assert response.status_code == 201

def test_login(client):
    data = {"email": "test@example.com", "password": "password"}
    response = client.post("/api/auth/login", json=data)
    assert response.status_code == 200

def test_get_user_details(client):
    response = client.get("/api/auth/user")
    assert response.status_code == 200