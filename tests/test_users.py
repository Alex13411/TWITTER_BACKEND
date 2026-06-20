def test_get_me_success(client, alice):
    """Авторизованный пользователь получает свой профиль."""
    response = client.get(
        "/api/users/me",
        headers={"api-key": "alice-key-123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert data["user"]["name"] == "Alice"
    assert data["user"]["followers"] == []
    assert data["user"]["following"] == []


def test_get_me_unauthorized(client):
    """Без api-key — ошибка 422."""
    response = client.get("/api/users/me")

    assert response.status_code == 422