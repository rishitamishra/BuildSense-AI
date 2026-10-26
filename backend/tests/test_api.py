from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get('/api/health')
    assert r.status_code == 200 and r.json()['status'] == 'ok'

def test_demo_analysis(monkeypatch):
    monkeypatch.delenv('GEMINI_API_KEY', raising=False)
    r = client.post('/api/analyze', data={'description':'Residential building','project_data':'{"built_up_area_sqft":1200,"floors":2,"cost_per_sqft_inr":1900}'})
    assert r.status_code == 200
    assert r.json()['mode'] == 'demo'
    assert r.json()['planning']['estimated_total_cost_inr'] == 2280000
