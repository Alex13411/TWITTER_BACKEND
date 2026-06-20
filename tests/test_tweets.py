def test_create_tweet(client, alice):
    """Пользователь создаёт твит."""
    response = client.post(
        "/api/tweets",
        headers={"api-key": "alice-key-123"},
        json={
            "tweet_data": "Мой тестовый твит",
            "tweet_media_ids": [],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert "tweet_id" in data


def test_feed_shows_following_tweets(client, alice, bob):
    """В ленте видны твиты тех, на кого подписан."""
    # Bob создаёт твит
    client.post(
        "/api/tweets",
        headers={"api-key": "bob-key-456"},
        json={"tweet_data": "Твит от Bob", "tweet_media_ids": []},
    )

    # Alice подписывается на Bob
    client.post(
        f"/api/users/{bob.id}/follow",
        headers={"api-key": "alice-key-123"},
    )

    # Alice смотрит ленту
    response = client.get(
        "/api/tweets",
        headers={"api-key": "alice-key-123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert len(data["tweets"]) == 1
    assert data["tweets"][0]["content"] == "Твит от Bob"
    assert data["tweets"][0]["author"]["name"] == "Bob"