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
def test_follow_success(client, alice, bob):
    """Alice подписывается на Bob."""
    response = client.post(
        f"/api/users/{bob.id}/follow",
        headers={"api-key": "alice-key-123"},
    )

    assert response.status_code == 200
    assert response.json()["result"] is True

    # Проверяем через профиль
    profile = client.get(
        "/api/users/me",
        headers={"api-key": "alice-key-123"},
    ).json()

    assert profile["user"]["following"][0]["name"] == "Bob"


def test_follow_self_fails(client, alice):
    """Нельзя подписаться на самого себя."""
    response = client.post(
        f"/api/users/{alice.id}/follow",
        headers={"api-key": "alice-key-123"},
    )

    assert response.status_code == 400
    assert response.json()["result"] is False
    assert response.json()["error_type"] == "BadRequest"