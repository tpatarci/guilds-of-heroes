"""API tests using httpx WSGITransport."""

from __future__ import annotations

import httpx
import pytest

from api.app import create_app
from config.settings import Settings


@pytest.fixture()
def settings(tmp_path) -> Settings:  # type: ignore[no-untyped-def]
    return Settings(
        GOH_ENV="testing",
        GOH_DB_PATH=str(tmp_path / "test.db"),
        GOH_SECRET_KEY="test-secret-key-minimum-32-chars!",
        GOH_JWT_SECRET="test-jwt-secret-minimum-32-chars!",
    )


@pytest.fixture()
def app(settings):  # type: ignore[no-untyped-def]
    return create_app(settings)


@pytest.fixture()
def client(app):  # type: ignore[no-untyped-def]
    transport = httpx.WSGITransport(app=app)  # type: ignore[arg-type]
    return httpx.Client(transport=transport, base_url="http://testserver")


def _register(client: httpx.Client, username: str = "testuser") -> dict:
    resp = client.post("/api/v1/auth/register", json={
        "username": username,
        "email": f"{username}@test.com",
        "password": "password123",
    })
    assert resp.status_code == 201
    return resp.json()


def _auth_header(data: dict) -> dict[str, str]:
    return {"Authorization": f"Bearer {data['access_token']}"}


class TestHealthAPI:
    def test_health(self, client: httpx.Client) -> None:
        resp = client.get("/api/v1/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_health_deep(self, client: httpx.Client) -> None:
        resp = client.get("/api/v1/health/deep")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["database"]["connected"] is True

    def test_correlation_id(self, client: httpx.Client) -> None:
        resp = client.get("/api/v1/health", headers={"X-Correlation-Id": "test-123"})
        assert resp.headers.get("X-Correlation-Id") == "test-123"


class TestAuthAPI:
    def test_register(self, client: httpx.Client) -> None:
        data = _register(client)
        assert data["user"]["username"] == "testuser"
        assert "access_token" in data

    def test_login(self, client: httpx.Client) -> None:
        _register(client)
        resp = client.post("/api/v1/auth/login", json={
            "username": "testuser", "password": "password123",
        })
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    def test_me(self, client: httpx.Client) -> None:
        data = _register(client)
        resp = client.get("/api/v1/auth/me", headers=_auth_header(data))
        assert resp.status_code == 200
        assert resp.json()["username"] == "testuser"

    def test_me_no_auth(self, client: httpx.Client) -> None:
        resp = client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    def test_refresh(self, client: httpx.Client) -> None:
        data = _register(client)
        resp = client.post("/api/v1/auth/refresh", json={
            "refresh_token": data["refresh_token"],
        })
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    def test_logout(self, client: httpx.Client) -> None:
        data = _register(client)
        resp = client.post("/api/v1/auth/logout", json={
            "refresh_token": data["refresh_token"],
        })
        assert resp.status_code == 200


class TestPostsAPI:
    def test_create_and_get_post(self, client: httpx.Client) -> None:
        auth = _register(client)
        headers = _auth_header(auth)

        resp = client.post("/api/v1/posts", json={"content": "Hello D&D!"}, headers=headers)
        assert resp.status_code == 201
        post = resp.json()

        resp = client.get(f"/api/v1/posts/{post['id']}")
        assert resp.status_code == 200
        assert resp.json()["content"] == "Hello D&D!"

    def test_timeline(self, client: httpx.Client) -> None:
        auth = _register(client)
        headers = _auth_header(auth)
        client.post("/api/v1/posts", json={"content": "Post 1"}, headers=headers)

        resp = client.get("/api/v1/posts/timeline")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1


class TestEventsAPI:
    def test_create_event(self, client: httpx.Client) -> None:
        auth = _register(client)
        headers = _auth_header(auth)

        resp = client.post("/api/v1/events", json={
            "title": "Dragon Hunt",
            "start_time": "2026-03-01T18:00:00",
            "max_players": 5,
        }, headers=headers)
        assert resp.status_code == 201
        assert resp.json()["title"] == "Dragon Hunt"

    def test_rsvp(self, client: httpx.Client) -> None:
        auth1 = _register(client, "dungeon_master")
        auth2 = _register(client, "player")

        resp = client.post("/api/v1/events", json={
            "title": "Game Night", "start_time": "2026-03-01",
        }, headers=_auth_header(auth1))
        event_id = resp.json()["id"]

        resp = client.post(
            f"/api/v1/events/{event_id}/rsvp",
            json={"status": "going"},
            headers=_auth_header(auth2),
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "going"


class TestDiceAPI:
    def test_roll(self, client: httpx.Client) -> None:
        auth = _register(client)
        resp = client.post("/api/v1/dice/roll", json={
            "expression": "1d20",
        }, headers=_auth_header(auth))
        assert resp.status_code == 200
        data = resp.json()
        assert 1 <= data["total"] <= 20

    def test_history(self, client: httpx.Client) -> None:
        auth = _register(client)
        headers = _auth_header(auth)
        client.post("/api/v1/dice/roll", json={"expression": "1d20"}, headers=headers)

        resp = client.get("/api/v1/dice/history", headers=headers)
        assert resp.status_code == 200
        assert len(resp.json()) == 1


class TestCampaignsAPI:
    def test_create_campaign(self, client: httpx.Client) -> None:
        auth = _register(client)
        resp = client.post("/api/v1/campaigns", json={
            "name": "Curse of Strahd",
        }, headers=_auth_header(auth))
        assert resp.status_code == 201
        assert resp.json()["name"] == "Curse of Strahd"

    def test_join_campaign(self, client: httpx.Client) -> None:
        dm = _register(client, "dungeon_master")
        player = _register(client, "player")

        resp = client.post("/api/v1/campaigns", json={
            "name": "Test Campaign",
        }, headers=_auth_header(dm))
        camp_id = resp.json()["id"]

        resp = client.post(
            f"/api/v1/campaigns/{camp_id}/join",
            headers=_auth_header(player),
        )
        assert resp.status_code == 200
        assert resp.json()["joined"] is True


class TestCharactersAPI:
    def test_create_character(self, client: httpx.Client) -> None:
        auth = _register(client)
        resp = client.post("/api/v1/characters", json={
            "name": "Gandalf",
            "race": "Human",
            "class": "Wizard",
            "level": 20,
        }, headers=_auth_header(auth))
        assert resp.status_code == 201
        assert resp.json()["name"] == "Gandalf"

    def test_my_characters(self, client: httpx.Client) -> None:
        auth = _register(client)
        headers = _auth_header(auth)
        client.post("/api/v1/characters", json={"name": "Char1"}, headers=headers)

        resp = client.get("/api/v1/characters/mine", headers=headers)
        assert resp.status_code == 200
        assert len(resp.json()) == 1


class TestErrorHandling:
    def test_404(self, client: httpx.Client) -> None:
        resp = client.get("/api/v1/nonexistent")
        assert resp.status_code == 404
        assert "correlation_id" in resp.json()

    def test_validation_error(self, client: httpx.Client) -> None:
        resp = client.post("/api/v1/auth/register", json={
            "username": "ab", "email": "a@b.com", "password": "password123",
        })
        assert resp.status_code == 400
        assert resp.json()["error"] == "VALIDATION_ERROR"
