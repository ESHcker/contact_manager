
def test_register(client):
    response = client.get("/auth/register")
    assert response.status_code == 200
