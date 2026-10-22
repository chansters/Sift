"""Categories + health tests."""

from httpx import AsyncClient
from sqlalchemy import select
from tests.conftest import setup_admin

from app.core.db import get_session
from app.models import SEED_CATEGORIES, Category


async def _seed_categories() -> None:
    async for s in get_session():
        existing = await s.scalar(select(Category.id).limit(1))
        if existing is None:
            s.add_all([Category(name=n) for n in SEED_CATEGORIES])
            await s.commit()
        break


async def test_health(client: AsyncClient) -> None:
    r = await client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    # Keep the established field while extending the response additively.
    assert body["version"] == "0.1.0"
    assert body["sift_version"] == "0.1.0"
    assert body["upstream_name"] == "NewsGator"
    assert body["upstream_version"] == "1.6.0"
    assert body["build_commit"] == "unknown"


async def test_health_reports_build_commit(client: AsyncClient, monkeypatch) -> None:
    monkeypatch.setenv("BUILD_COMMIT", "a1b2c3d4e5f6")
    r = await client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["build_commit"] == "a1b2c3d4e5f6"


async def test_categories_crud(client: AsyncClient) -> None:
    await setup_admin(client)
    await _seed_categories()

    r = await client.get("/api/categories")
    names = [c["name"] for c in r.json()]
    assert "Tech" in names and "Uncategorized" in names

    r = await client.post("/api/categories", json={"name": "AI"})
    assert r.status_code == 201
    cat_id = r.json()["id"]

    r = await client.post("/api/categories", json={"name": "AI"})
    assert r.status_code == 409

    r = await client.patch(f"/api/categories/{cat_id}", json={"name": "AI & ML"})
    assert r.json()["name"] == "AI & ML"

    r = await client.delete(f"/api/categories/{cat_id}")
    assert r.status_code == 204

    # 'Uncategorized' is protected
    r = await client.get("/api/categories")
    unc = next(c for c in r.json() if c["name"] == "Uncategorized")
    assert (await client.delete(f"/api/categories/{unc['id']}")).status_code == 400
