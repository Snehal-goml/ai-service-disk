
import pytest
from app.main import ready


# ── Ready endpoint (async, uses real DB session) ───────────────────────────────

@pytest.mark.asyncio
async def test_ready_returns_dict(db_session):
    res = await ready(db_session)
    assert isinstance(res, dict)


@pytest.mark.asyncio
async def test_ready_status_is_ok(db_session):
    res = await ready(db_session)
    assert res.get("status") == "ok"


@pytest.mark.asyncio
async def test_ready_database_is_connected(db_session):
    res = await ready(db_session)
    assert res.get("database") == "connected"


@pytest.mark.asyncio
async def test_ready_returns_exactly_two_keys(db_session):
    res = await ready(db_session)
    assert set(res.keys()) == {"status", "database"}


@pytest.mark.asyncio
async def test_ready_values_are_strings(db_session):
    res = await ready(db_session)
    assert isinstance(res["status"], str)
    assert isinstance(res["database"], str)